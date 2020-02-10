#include <math.h>
int randNumber;
int calis = false;
int r = false;
int total = 0;
int puan = 0;
int top = 0;
int ResPin = 7;
int s = 1;
unsigned long zaman_1 = 0;
unsigned long zaman_2 = 0;

void setup() {
  Serial.begin(4800);
  digitalWrite(ResPin, HIGH);
  pinMode(ResPin, OUTPUT);
}

void loop() {

  Serial.setTimeout(400);
  randomSeed(random(1, 1000));
  String s1 = Serial.readString();
  if (s1.indexOf("RUN") >= 0) {
    calis = true;
    delay(1000);
    r = true;
    //s = 0;
    total = 0;
    top = 0;
  }

  if (calis == true && r == true) {
    //randNumber = random(1, 21);
    randNumber = s++;
    Serial.println("LED=" + String(randNumber) + "," + String(2));
    zaman_1 = millis();
    calis = false;
    if (randNumber != 0) {
      //Serial.println("L");
    }
    delay(1000);
  }

  if (s1.indexOf("B=" + String(randNumber) + "," + String(1)) >= 0) {
    Serial.println("LED=" + String(randNumber) + "," + String(3));
    zaman_2 = millis();
    top = (zaman_2 - zaman_1) / 1000;
    puan = ceil(20 * exp(-top / 2));
    total = total + puan;
    //Serial.println(total);
    calis = true;
    if (randNumber != 0) {
      //Serial.println("B");
    }
    delay(1000);
  }

  if (s1.indexOf("STOP") >= 0) {
    r = false;
    Serial.println("LED=" + String(randNumber) + "," + String(3));
  }
  if (s1.indexOf("PUAN") >= 0) {
    for (int i = 1; i <= 3; i++){
    Serial.println(total);
    delay(100);
  }
  }

  if (s1.indexOf("RESET") >= 0 ) {
    digitalWrite(ResPin, LOW);
  }

  if (s1.indexOf("LED") >= 0) {
    for ( int p = 1; p <= 20; p++) {
      Serial.println("LED=" + String(p) + "," + String(2));
      delay(50);
    }
    delay(200);
    for ( int k = 1; k <= 20; k++) {
      Serial.println("LED=" + String(k) + "," + String(3));
      delay(50);
    }
    delay(200);

  }

}
