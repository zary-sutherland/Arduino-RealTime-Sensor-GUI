#include <Wire.h>
#include <I2C_Anything.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

volatile float h;
volatile float t;
String flag = "0";
void setup() {
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(115200);  // start serial for output
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(true,true); // gyro and accelero
  Serial.println("Done!\n");
//  flag = "2";
}

void loop() {
  mpu.update();
  while (Serial.available() > 0){
      flag = Serial.readString();
      Serial.print(flag);
  }

  if(flag == "DHT11"){
  Wire.requestFrom(8, 32);    // request 32 bytes from slave device #8
  }

  if(flag == "MPU6050"){
    Serial.print("X ");
    Serial.print(mpu.getAngleX());
    Serial.print(" Y ");
    Serial.println(mpu.getAngleY());
  }
  
  while (Wire.available() && flag == "DHT11"){ // slave may send less than requested
    I2C_readAnything(h);
    I2C_readAnything(t);
    if (!isnan(h) && !isnan(t)){
        Serial.print("Temperature ");
        Serial.print(t);
        Serial.print(" Humidity ");
        Serial.println(h);
    }
  }

  delay(1000);
}
