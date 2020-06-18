#include <math.h> // Kütüphane tanımlamaları

int randNumber;     // random sayı değişken tanımlaması
int calis = false;  // başlat komut şartını sağlayan değişken
int r = false;      // stop komut şartını sağlayan değişken
int total = 0;      // toplam puan değişkeni
int puan = 0;       // anlık puan değişkeni
int Dt = 0;         // iki panel arasında ki süre farkı (sn)
String LED_ON;      // Panel Led on ışık satırı
String LED_OFF;     // Panel Led off ışık satırı
String STOP;
int count = 0;      // sayaç değişkeni
int b = 0;          // panel durum değişken sayacı
int ilk_panel;      // ilk panel değişkeni
int son_panel;      // son panel değişkeni
int fark;           // ilk-son panel değişkeni
int a = false;
int c = true;
unsigned long t1 = 0; // ilk panel süresi
unsigned long t2 = 0; // son panel süresi
int k = 0;            // puan katsayısı
int K = 20;           // puan katsayısı


void setup() {
  Serial.begin(4800); // bant tanımlaması (paneller ile aynı olmalı)

}

void loop() {

  Serial.setTimeout(350);           // loop yenilenme süresi
  randomSeed(random(1, 1000));      // random matris değişkeni
  String s1 = Serial.readString();  // string veri okuma


  if (s1.indexOf("RUN") >= 0) {     // RUN yazısı seri port'a gelirse if şartı sağlansın
    calis = true;
    r = true;                       // STOP komutu şartı
    a = true;
    c = false;
    total = 0;
    Dt = 0;
    puan = 0;
    fark = 0;
  }

  if (calis == true && r == true) { // bir önceki şart (calis=true) sağlanırsa random sayı üretilsin
    randNumber = random(1, 21);
    LED_ON = "LED=" + String(randNumber) + "," + String(2);
    Serial.println(LED_ON);
    t1 = millis();
    b++;
    count++;
    if (b == 1) {
      ilk_panel = randNumber;
    }
    a = true;
    calis = false;
  }

  if (s1.indexOf("B=" + String(randNumber) + "," + String(1)) >= 0) {

    LED_OFF = "LED=" + String(randNumber) + "," + String(3);
    Serial.println(LED_OFF);
    t2 = millis();
    Dt = (t2 - t1) / 1000;
    calis = true;
    if (b == 2) {
      son_panel = randNumber;
      fark = ilk_panel - son_panel;
      b = 0;
    }

    if (abs(fark) == 10) {
      k = 2;
      puan = k * ceil(K * exp(-Dt / 2));
      total = total + puan;

    }
    else if (fark == 0) {
      k = 1;
      puan = k * ceil(K * exp(-Dt / 2));
      total = total + puan;

    }
    else if (abs(fark) < 10 && fark > 0) {
      k = 1 + abs(fark) / 10;
      puan = k * ceil(K * exp(-Dt / 2));
      total = total + puan;

    }
    else if (abs(fark) < 10 && fark < 0) {
      k = 1 + abs(fark) / 10;
      puan = k * ceil(K * exp(-Dt / 2));
      total = total + puan;

    }
    else if (abs(fark) > 10 && fark < 0) {
      k = 3 - abs(fark) / 10;
      puan = k * ceil(K * exp(-Dt / 2));
      total = total + puan;

    }
    else if (abs(fark) > 10 && fark > 0) {
      k = 3 - abs(fark) / 10;
      puan = k * ceil(K * exp(-Dt / 2));
      total = total + puan;

    }

    a = false;
  }


  if (s1.indexOf("STOP") >= 0) {

    r = false;
    STOP = "LED=" + String(randNumber) + "," + String(3);
    Serial.println(STOP);
    a = false;


  }
  if (s1.indexOf("PUAN") >= 0) {
    for (int i = 1; i <= 3; i++) {
      Serial.println(total);
      delay(100);
    }
  }

  if (s1.indexOf("LED") >= 0) {

    for ( int p = 1; p <= 20; p++) {

      String LED_P = "LED=" + String(p) + "," + String(3);
      Serial.println(LED_P);
      delay(50);
    }
    delay(200);
    for ( int k = 1; k <= 20; k++) {

      String LED_K = "LED=" + String(k) + "," + String(3);
      Serial.println(LED_K);
      delay(50);
    }
    delay(200);

  }

}
