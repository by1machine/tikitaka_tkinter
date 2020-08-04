#include <EEPROM.h>


int isim_addr = 0;


String mesaj = "";
int myledpin1 = 11;
int myledpin = 10;
int mybuttonpin = 13;
int oncekibuttondeger = 0;
int myindex = 1;
int sensora0 = A0;
int sensoranalogdurum = -1;
int sensorkatsayi = 20;
long previousMillis = 0;        // will store last time LED was updated
long interval = 600;
int ledyanikmi = false;
int btncakismaizin = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(4800);
  pinMode(mybuttonpin, INPUT_PULLUP);
  myindex = EEPROM.read(isim_addr);
  if (myindex > 25)myindex = 0;
  //pinMode(myledpin,OUTPUT);
  //digitalWrite(myledpin,HIGH);


  pinMode(myledpin, INPUT);
  digitalWrite(myledpin, 0);
  pinMode(myledpin1, INPUT);
  digitalWrite(myledpin1, 0);

  ledyanikmi = false;
  sensoranalogdurum = analogRead(A0);
  for (int x = 0; x < 4; x++)
  {
    sensoranalogdurum = sensoranalogdurum + analogRead(A0);
    sensoranalogdurum = sensoranalogdurum / 2;
    delay(5);
  }
  if (sensoranalogdurum > 500) {
    sensorkatsayi = 100;
  } else if (sensoranalogdurum > 100) {
    sensorkatsayi = 40;
  } else if (sensoranalogdurum > 50) {
    sensorkatsayi = 20;
  } else if (sensoranalogdurum > 10) {
    sensorkatsayi = 6;
  }
  delay(myindex * 400);

  Serial.println("S:" + String(myindex) + "," + String(sensoranalogdurum) + "," + String(sensorkatsayi));
}

void loop() {
  // put your main code here, to run repeatedly:


  while (Serial.available() > 0  ) {
    char gelen = Serial.read();
    if (gelen == char(10)) {

      //  Serial.println(mesaj);
      // userinterface(mesaj);
      if (mesaj.indexOf("NAME=") == 0)
      {
        myindex = mesaj.substring(5).toInt();
        EEPROM.write(isim_addr, myindex);
        Serial.println("OK");
      }
      if (mesaj.indexOf("LED=") == 0) {
        String led_bilgi = mesaj.substring(4);
        int led_index = led_bilgi.substring(0, led_bilgi.indexOf(",")).toInt();
        int led_deger = led_bilgi.substring(led_bilgi.indexOf(",") + 1).toInt();
        if (led_index == myindex) {
          if (led_deger == 0 || led_deger == 1) {
            digitalWrite(myledpin, led_deger);
            digitalWrite(myledpin1, led_deger);

            Serial.println("OK");
          }
          if (led_deger == 2 ) {
            pinMode(myledpin, OUTPUT);
            pinMode(myledpin1, OUTPUT);

            //Serial.println("OK");
            ledyanikmi = true;
          }
          if (led_deger == 3 ) {
            pinMode(myledpin, INPUT);

            pinMode(myledpin1, INPUT);

            //Serial.println("OK");
            ledyanikmi = false;
          }
        }
        if (led_deger == 8)
        {
          btncakismaizin = true;
        }

        if (led_deger == 9)
        {
          btncakismaizin = false;
        }

      } else {
        // Serial.println("error:"+mesaj);
      }

      mesaj = "";
    }
    else {
      mesaj += gelen;
    }
  }
  unsigned long currentMillis = millis();

  //  int a0val = analogRead(A0);
  // Serial.println(a0val);
  //    if(a0val<sensoranalogdurum-sensorkatsayi ){
  //      if(oncekibuttondeger==0){
  //          if(currentMillis - previousMillis > interval) {
  //            previousMillis = millis();
  //              Serial.println("B="+String(myindex)+","+String(1));
  //
  //         }
  //        }
  //        oncekibuttondeger=1;
  //      }else{
  //        oncekibuttondeger=0;
  //        }

  int buttondeger = digitalRead(mybuttonpin);

  if (buttondeger != oncekibuttondeger) {
    //   Serial.println("BUTTON="+String(myindex)+","+"1");

    if (buttondeger == 0) {

      if (currentMillis - previousMillis > interval) {

        if (btncakismaizin == true) {
          if (ledyanikmi == true) {

            previousMillis = millis();

            Serial.println("B=" + String(myindex) + "," + String(1));

          }
        } else {

          previousMillis = millis();

          Serial.println("B=" + String(myindex) + "," + String(1));

        }
      }
    }
    oncekibuttondeger = buttondeger;

  }
  delay(10);
}
