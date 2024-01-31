#ifndef _HB100_HH_
#define _HB100_HH_

#include "stdint.h"
#include "kiss_fft.h"

class HB100 {
public:
    struct HB100Config {
        uint16_t adc_in_pin = 28;
        uint16_t adc_in_channel = 2;
        // 99mph is 3.104kHz, Nyquist says we need to sample 6.208kHz to resolve.
        // ADC Clock is 48MHz, each conversion takes 96 cycles.
        // Divider DIV sets ADC to start sampling every DIV+1 cycles.
        // Thus DIV >= 95.
        // For 6.208kHz ADC sample rate, divider should be 7731. Set to 7000 to be safe.
        uint16_t adc_clk_div = 6e3;
        uint16_t adc_buf_num_samples = 1e3; // number of samples per DMA buffer
        uint16_t capture_status_led = 25;
    };

    HB100(HB100Config config_in);
    ~HB100(); // destructor

    void Init();
    void Update();

private:
    HB100Config config_;
    uint32_t dma_chan1_;
    uint32_t dma_chan2_;
    uint16_t * adc_dma_buf1_;
    uint16_t * adc_dma_buf2_;
    uint16_t * fft_dma_buf_;
    kiss_fft_cpx * fft_out_buf_;

    kiss_fft_cfg fft_cfg_;

    void ComputeFFT_();
};

#endif