#include <SoftwareSerial.h>

SoftwareSerial bluetooth(3, 2); // rx, tx
const int gndBluetooth = 4;
const int vccBluetooth = 5;

const int GSR = A1;
////const int vccGSR = A1;
////const int gndGSR = A2;
int gsr_value = 0;
int gsr_average = 0;

//const int AIMP = A0;
//////const int AIMP = A1;
//////const int gndMP = A4;
//////const int vccMP = A5;
//int mp_value = 0;
//int mp_average = 0;

//int cnt = 0;
//String str_gsr = "";
//String str_mp = "";

void setup()
{
    Serial.begin(9600);
    bluetooth.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);

    //  pinMode(vccBluetooth, OUTPUT);
    //  digitalWrite(vccBluetooth, HIGH);
    //  pinMode(gndBluetooth, OUTPUT);
    //  digitalWrite(gndBluetooth, LOW);

    //  pinMode(vccGSR, OUTPUT);
    //  digitalWrite(vccGSR, HIGH);
    //  pinMode(gndGSR, OUTPUT);
    //  digitalWrite(gndGSR, LOW);

    //  pinMode(vccMP, OUTPUT);
    //  digitalWrite(vccMP, HIGH);
    //  pinMode(gndMP, OUTPUT);
    //  digitalWrite(gndMP, LOW);
}

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    long gsr_sum = 0;
//    long mp_sum = 0;
    
    //Average the 5 measurements to remove the glitch
    for (int i = 0; i < 5; i++)
    {
        gsr_value = analogRead(GSR);
//        mp_value = analogRead(AIMP);
        gsr_sum += gsr_value;
//        mp_sum += mp_value;
        delay(5);
    }
    gsr_average = gsr_sum / 5;
//    mp_average = mp_sum / 5;

//      gsr_value = analogRead(GSR);
//    //  float gsr_voltage= gsr_value * (5.0 / 1023.0);
//      mp_value = analogRead(AIMP);

    digitalWrite(LED_BUILTIN, LOW);
//    Serial.print("#");
    Serial.print(gsr_average);
//    Serial.print("#");
//    Serial.print(mp_average);
    Serial.println();

//      Serial.print("#");
//      Serial.print(cnt);
//      Serial.print("#");
//      Serial.print(gsr_value, HEX);
//      Serial.print("#");
//      Serial.print(mp_value, HEX);
//      Serial.println();

    bluetooth.print("#");
    bluetooth.print(gsr_average);
//    bluetooth.print("#");
//    bluetooth.print(mp_average);
    bluetooth.println();

//      cnt++;
//      if (cnt >= 100) {
//        str_gsr = str_gsr+String(gsr_value);
//        str_mp = str_mp+String(mp_value);
//
//        Serial.print(str_gsr);
//        Serial.print("#");
//        Serial.print(str_mp);
//        Serial.println();
//        
//        bluetooth.print(str_gsr);
//        bluetooth.print("#");
//        bluetooth.print(str_mp);
//        bluetooth.println();
//        str_gsr = "";
//        str_mp = "";
//        cnt = 0;
//      } else {
//        str_gsr = str_gsr+String(gsr_value)+";";
//        str_mp = str_mp+String(mp_value)+";";
//      }

//      bluetooth.print("#");
//      bluetooth.print(cnt);
//      bluetooth.print("#");
//      bluetooth.print(gsr_value, HEX);
//      bluetooth.print("#");
//      bluetooth.print(mp_value, HEX);
//      bluetooth.print("#b");
//      bluetooth.println();
      delay(10);
//      cnt++;

    //  Serial.println(gsr_average);
    //  bluetooth.println(gsr_average);
}