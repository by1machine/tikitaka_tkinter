#include <math.h>

long randNumber;

int calis = false;
int r = false;
int total = 0;
int puan = 0;
int s = 0;
int top = 0;
int ResPin = 7;

unsigned long zaman_1 = 0;
unsigned long zaman_2 = 0;

void setup() 
{
  Serial.begin(4800);
  digitalWrite(ResPin, HIGH);
  pinMode(ResPin, OUTPUT);
}

void loop() 
{
  randomSeed(random(1, 1000));
  String s1 = Serial.readString();
  if (s1.indexOf("RUN") >= 0) {
    calis = true;
    delay(1000);
    r = true;
    s = 0;
    total = 0;
    top = 0;
  }
  
  if (calis == true && r == true) {
    randNumber = random(1, 21);
    Serial.println("LED=" + String(randNumber) + "," + String(2));
    zaman_1 = millis();
    calis = false;
  }
  
  if (s1.indexOf("B=" + String(randNumber) + "," + String(1)) >= 0) {
    Serial.println("LED=" + String(randNumber) + "," + String(3));
    zaman_2 = millis();
    top = (zaman_2 - zaman_1) / 1000;
    puan = ceil(20 * exp(-top / 2));
    total = total + puan;
    calis = true;
    s++;
  }
  delay(50);
  
  if (s1.indexOf("STOP") >= 0) {
    r = false;
    Serial.println("LED=" + String(randNumber) + "," + String(3));
    Serial.println(total);
    Serial.println(s);
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
    }
}
