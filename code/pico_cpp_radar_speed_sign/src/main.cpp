#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/binary_info.h"

#include "hb100.hh"

const uint16_t kLEDPin = 25;

HB100 * hb100;

int main() {
    bi_decl(bi_program_description("Pico CPP Radar Speed Sign"));

    stdio_init_all();

    printf("Hello World\r\n");

    HB100::HB100Config hb100_config;
    hb100 = new HB100(hb100_config);

    hb100->Init();

    while (true) {
        hb100->Update();
    }

}