#include "DHT.h"

#define DHTPIN A1
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  
  Serial.begin(9600);
  dht.begin();

}

void loop() {
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("Umidade: ");
  Serial.print(h);
  Serial.print(" | ");
  Serial.print("Temperatura: ");
  Serial.print(t);
  Serial.println("");
  delay(10000);

}