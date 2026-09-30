#include <OneWire.h>
#include <DallasTemperature.h>
#define TEMP_PIN 4
#define WATER_PIN 32
#define TDS_PIN 34
#define PH_PIN 35
OneWire oneWire(TEMP_PIN);
DallasTemperature temperatureSensor(&oneWire);
void setup() {
  Serial.begin(115200);
  temperatureSensor.begin();
  delay(1000);
  Serial.println("================================");
  Serial.println("Smart Aquaculture Assistant");
  Serial.println("ESP32 Sensor Monitoring Started");
  Serial.println("================================");
}
void loop() {
  temperatureSensor.requestTemperatures();
  float temperature =
      temperatureSensor.getTempCByIndex(0);
  int waterValue = analogRead(WATER_PIN);
  int tdsRaw = analogRead(TDS_PIN);
  float tdsVoltage =
      tdsRaw * 3.3 / 4095.0;
  int phRaw = analogRead(PH_PIN);
  float pH =
      7.0 + (2130 - phRaw) * 0.003;
  Serial.println("-------------------------");
  Serial.print("Temperature: ");
  Serial.print(temperature, 2);
  Serial.println(" C");
  Serial.print("Water Sensor: ");
  Serial.println(waterValue);
  Serial.print("TDS Voltage: ");
  Serial.print(tdsVoltage, 2);
  Serial.println(" V");
  Serial.print("pH: ");
  Serial.println(pH, 2);
  Serial.println("-------------------------");
  delay(2000);
}
