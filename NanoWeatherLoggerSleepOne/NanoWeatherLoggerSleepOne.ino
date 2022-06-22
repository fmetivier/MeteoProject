/*
 * Libraries, constants and variables
 */


// DHT sensor lib
#include <DHT_U.h>
#include <DHT.h>
#define DHT_TYPE DHT11
#define DHT_PIN 7
DHT dht(DHT_PIN,DHT_TYPE);

//SD Card lib
#include <SPI.h>
#include <SD.h>

//RTC lib
#include <Wire.h>
#include <RTClib.h>
#define ADRESSE_I2C_RTC 0x68 // RTC card address
RTC_DS1307 rtc;

//Power management
#include <LowPower.h>



const int chipSelect = 10; // SD card on Nano
const byte pluvio = 2;  // pullup for pluviometer on D2
volatile int counter = 0;


void setup()
{
  //Serial Initialization
  Serial.begin(9600); 

  // DH11 initialization
  dht.begin();

  
  /*
   * Pluviometer initialization
   * Because we just want to count the number of auger tilts 
   * we place the attachinterrupt un the setup
   */
  pinMode(pluvio, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pluvio), pCount, FALLING);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  /*
   * RTC initialization
   * DO NOT synchronize here 
   * because If the arduino restarts it will also reinitialize the clock...
   * Thanks Olivier !
   */
  Wire.begin();
  Wire.beginTransmission(ADRESSE_I2C_RTC);

  while (!rtc.begin()){
      Serial.println("Attente module HTR");
      delay(1000);
  }

  Wire.endTransmission();

  /*
   * SD Card
   */
  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
  }
  else {
    Serial.println("card initialized.");
  }

}

void loop()
{

  /*
   * Get time, T and H
   */
  Wire.beginTransmission(ADRESSE_I2C_RTC);
  DateTime now = rtc.now();
  Wire.endTransmission();
  
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  /*
   * Make the string to be written to SD card
   */
  char sdate[12];
  sprintf(sdate,"%04d:%02d:%02d",now.year(),now.month(),now.day());
  char stime[10];
  sprintf(stime,"%02d:%02d:%02d",now.hour(),now.minute(),now.second());
  
  String dataString =  "w,";
  dataString +=  String(sdate) + "," + String(stime) + "," + String(t) + "," + String(h) + "," + String(counter*0.25) + "\n";
  Serial.print(dataString);

  writeData(dataString);
  /*
   * set rain coutner to 0
   */
  counter = 0;

 /*
  * Go to sleep fro one minute
  */
 for (int i=1;i<=7;i++){ // change to 1 for 12s
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
  }
 LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF); 
}


/*
 * write data to SD card
 */
void writeData(String dataString)
{
  if (SD.begin(chipSelect)){
  
     File dataFile = SD.open("METEOLOG.TXT", FILE_WRITE);
  
     // if the file is available, write to it:
     if (dataFile) {
      dataFile.print(dataString);
      dataFile.close();
     }
     // if the file isn't open, pop up an error:
     else {
       Serial.println("error opening METEOLOG.TXT");
     }
   }
   else{
    Serial.println("No card available. Loosing data");
   }
}


/*
 * Counter that stores the number of auger tilts during sleep
 */
void pCount()
{

  counter += 1;
  
}
