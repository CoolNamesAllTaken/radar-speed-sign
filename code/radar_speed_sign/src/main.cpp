#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ClickEncoder.h>
#include <EEPROM.h>
#include <TimerOne.h>

#include "seven_seg.hh"
#include "hb100.hh"

#define RADAR_PIN 2

#define LCD_ADDRESS 0x27
#define LCD_WIDTH_CHARS 16
#define LCD_HEIGHT_LINES 2

#define ENCODER_PIN_A A1
#define ENCODER_PIN_B A0
#define ENCODER_PIN_BTN A2
#define ENCODER_STEPS_PER_NOTCH 1


volatile uint32_t last_pulse_ms = millis(); // [ms] time of last radar pulse
volatile uint32_t last_pulse_period = 0; // [ms] time between last two falling edges from radar

LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_WIDTH_CHARS, LCD_HEIGHT_LINES);
ClickEncoder* encoder;

SevenSeg seven_seg; // 7-segment display
HB100 hb100; // radar

void timer1_isr() {
  encoder->service();
}

/**
 * Interrupt handler that triggers on falling pulses from HB100 radar
 **/
void radar_isr() {
  hb100.last_pulse_period = millis() - hb100.last_pulse_ms;
  hb100.last_pulse_ms = millis();
}

void setup() {
  Serial.begin(9600);

  // Initialize radar.
  pinMode(RADAR_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(RADAR_PIN), radar_isr, FALLING);

  // Initialize 7-segment display.
  seven_seg.init();

  // Initialize LCD.
  lcd.init(); // initialize the lcd
	lcd.backlight();
	lcd.setCursor(0,0);
  lcd.clear();

  // Initialize encoder.
  encoder = new ClickEncoder(ENCODER_PIN_A, ENCODER_PIN_B, ENCODER_PIN_BTN, ENCODER_STEPS_PER_NOTCH);
  Timer1.initialize(500);
	Timer1.attachInterrupt(timer1_isr);
}

void loop() {
  // put your main code here, to run repeatedly:
  uint16_t transfer_value = 0;
  while (true) {
    transfer_value = hb100.calc_speed();
    // Serial.print("HB100 last pulse period: ");
    // Serial.println(hb100.last_pulse_period);
    // Serial.print("Calculated speed: ");
    Serial.println(hb100.calc_speed());
    seven_seg.write(hb100.calc_speed());
    delay(10);
    // transfer_value++;
    // if (transfer_value > 99) {
    //   transfer_value = 0;
    // }
  }
}

