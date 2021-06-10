#include <I2C_Anything.h>
#include "DHT.h"
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
#include <Wire.h>
DHT dht(DHTPIN, DHTTYPE);

volatile float h = 0.0f;
volatile float t = 0.0f;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("DHTxx test!");

  dht.begin();
  delay(2000);
  
  Wire.begin(8);
  Wire.onRequest(requestEvent);
}

void loop() {
//  float h = dht.readHumidity();
//  float t = dht.readTemperature();
  Serial.print(h);
  Serial.print("  ");
  Serial.println(t);
// put your main code here, to run repeatedly:
     h = dht.readHumidity();
    // Read temperature as Celsius (the default)
     t = dht.readTemperature();;
  delay(1000);
}

void requestEvent() {
  I2C_writeAnything(h) ;
  I2C_writeAnything(t) ;
//    char stringToSend[30];
//    char tem[5];
//    char hum[5];
//    char brk[2] = " | ";
//    dtostrf(t,4,4,tem);
//    dtostrf(h,4,4,hum);
//    strcpy(stringToSend,tem);
//    strcat(stringToSend, brk);
//    strcat(stringToSend,hum);
//    Wire.write(stringToSend);
//    Wire.write(tem);
//    Wire.write('|');
//    Wire.write(hum);
//    Wire.write(';');
}
