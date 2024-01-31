#include "hb100.hh"

#include "hardware/adc.h"
#include "hardware/dma.h"
#include "malloc.h"
#include "stdio.h"

HB100::HB100(HB100Config config_in) 
: config_(config_in)
, fft_dma_buf_(NULL)
{
    // Note: Malloc allocates Bytes.
    // ADC captures are 12 bits and stored as uint16_t's, which are aligned to 32 bits.
    adc_dma_buf1_ = (uint16_t *)malloc(4*config_.adc_buf_num_samples);
    adc_dma_buf2_ = (uint16_t *)malloc(4*config_.adc_buf_num_samples);

    static_assert(sizeof(kiss_fft_scalar) == sizeof(int16_t));
    fft_out_buf_ = (kiss_fft_cpx *)malloc(config_.adc_buf_num_samples * sizeof(kiss_fft_cpx));

    // Memset sets Bytes.
    memset(adc_dma_buf1_, 0, 4*config_.adc_buf_num_samples);
    memset(adc_dma_buf2_, 0, 4*config_.adc_buf_num_samples);

    fft_cfg_ = kiss_fft_alloc(
        config_.adc_buf_num_samples, // num FFT samples
        false, // not an inverse FFT
        0, // memory start address (set to 0 to let KISS FFT handle it)
        0 // memory length (set to 0 to let KISS FFT handle it)
    );
}

void HB100::Init() {

    gpio_init(config_.capture_status_led);
    gpio_set_dir(config_.capture_status_led, GPIO_OUT);

    adc_init();
    adc_select_input(config_.adc_in_channel);

    adc_fifo_setup(
        true,    // Write each completed conversion to the sample FIFO
        true,    // Enable DMA data request (DREQ)
        1,       // DREQ (and IRQ) asserted when at least 1 sample present
        false,   // Don't set ERR in bit 15 of each sample.
        false     // Don't shift each sample to 8 bits when pushing to FIFO
    );

    // Divisor of 0 -> full speed. Free-running capture with the divider is
    // equivalent to pressing the ADC_CS_START_ONCE button once per `div + 1`
    // cycles (div not necessarily an integer). Each conversion takes 96
    // cycles, so in general you want a divider of 0 (hold down the button
    // continuously) or > 95 (take samples less frequently than 96 cycle
    // intervals). This is all timed by the 48 MHz ADC clock.
    adc_set_clkdiv(config_.adc_clk_div);

    // Set up the DMA to start transferring data as soon as it appears in FIFO
    dma_chan1_ = dma_claim_unused_channel(true);
    dma_chan2_ = dma_claim_unused_channel(true);

    dma_channel_config cfg1 = dma_channel_get_default_config(dma_chan1_);
    dma_channel_config cfg2 = dma_channel_get_default_config(dma_chan2_);

    // Reading from constant address, writing to incrementing byte addresses
    channel_config_set_transfer_data_size(&cfg1, DMA_SIZE_16);
    channel_config_set_read_increment(&cfg1, false);
    channel_config_set_write_increment(&cfg1, true);
    channel_config_set_transfer_data_size(&cfg2, DMA_SIZE_16);
    channel_config_set_read_increment(&cfg2, false);
    channel_config_set_write_increment(&cfg2, true);

    // DMA channels are set to ping-pong, but not continuously.
    //  1.  Channel 1 starts.
    //  2.  Channel 1 completes.
    //  3.  FFT kicks off channel 2, begins processing channel 1 buffer.
    //  4. Channel 2 completes.
    //  5. FFT completes.
    //  6. FFT kicks off channel 1, begins processing channel 2 buffer.
    //  7. Channel 1 completes.
    //  8. FFT completes. Repeat fromn 3.

    // Chain DMAs to each other.
    // channel_config_set_chain_to(&cfg1, dma_chan2_);
    // channel_config_set_chain_to(&cfg2, dma_chan1_);

    // Set both DMA channels to trigger IRQ0 when they complete.
    dma_channel_set_irq0_enabled(dma_chan1_, true);
    dma_channel_set_irq0_enabled(dma_chan2_, true);

    // Pace transfers based on availability of ADC samples
    channel_config_set_dreq(&cfg1, DREQ_ADC);
    channel_config_set_dreq(&cfg2, DREQ_ADC);
    

    dma_channel_configure(dma_chan1_, &cfg1,
        adc_dma_buf1_,    // dst
        &adc_hw->fifo,  // src
        config_.adc_buf_num_samples,  // transfer count
        false            // don't start yet
    );
    dma_channel_configure(dma_chan2_, &cfg2,
        adc_dma_buf2_,    // dst
        &adc_hw->fifo,  // src
        config_.adc_buf_num_samples,  // transfer count
        false            // don't start yet
    );

    printf("Starting capture\n");
    adc_run(true);

    gpio_put(config_.capture_status_led, true);
    dma_start_channel_mask(1u << dma_chan1_); // Start DMA channel 1.
    // Make sure channel 1 is filled with data so we can go straight to FFT.
    dma_channel_wait_for_finish_blocking(dma_chan1_);
    gpio_put(config_.capture_status_led, false);
    fft_dma_buf_ = adc_dma_buf1_;
}

void HB100::Update() {
    // NOTE: This method assumes that the FFT computation interval takes longer than the ADC data collection interval
    // that runs via DMA.

    // Kick off ADC data collection on DMA channel not being used for FFT.
    uint16_t * next_fft_dma_buf_ = NULL;
    if (fft_dma_buf_ == adc_dma_buf1_) {
        dma_channel_set_write_addr(dma_chan2_, adc_dma_buf2_, true);
        next_fft_dma_buf_ = adc_dma_buf2_;

        dma_channel_wait_for_finish_blocking(dma_chan1_);
        printf("adc_dma_buf1=\r\n");
        for (uint16_t i = 0; i < config_.adc_buf_num_samples; i++) {
            printf("%d ", adc_dma_buf1_[i]);
        }
        printf("\r\n");
    } else {
        dma_channel_set_write_addr(dma_chan1_, adc_dma_buf1_, true);
        next_fft_dma_buf_ = adc_dma_buf1_;

        dma_channel_wait_for_finish_blocking(dma_chan2_);
        printf("adc_dma_buf2=\r\n");
        for (uint16_t i = 0; i < config_.adc_buf_num_samples; i++) {
            printf("%d ", adc_dma_buf2_[i]);
        }
        printf("\r\n");
    }

    // printfs are good placeholder for FFT time delay.

    fft_dma_buf_ = next_fft_dma_buf_; // prepare to look at the other DMA buffer next time.
}

HB100::~HB100() {
    free(adc_dma_buf1_);
    free(adc_dma_buf2_);
}