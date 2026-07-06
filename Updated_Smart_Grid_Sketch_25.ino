const int SOLAR_PIN = A0;  
const int WIND_PIN = A1;   

const int LED_HOSPITAL = 2;    
const int LED_RESIDENTIAL = 3; 
const int LED_INDUSTRIAL = 4;  
const int LED_COMMERCIAL = 5;  

float solarVoltage = 0.00;
float windVoltage = 0.00;
float totalVoltage = 0.00;

void setup() {
  Serial.begin(9600);
  pinMode(SOLAR_PIN, INPUT);
  pinMode(WIND_PIN, INPUT);
  pinMode(LED_HOSPITAL, OUTPUT);
  pinMode(LED_RESIDENTIAL, OUTPUT);
  pinMode(LED_INDUSTRIAL, OUTPUT);
  pinMode(LED_COMMERCIAL, OUTPUT);
}

void loop() {
  int rawSolar = analogRead(SOLAR_PIN);
  int rawWind = analogRead(WIND_PIN);
  
  solarVoltage = (rawSolar * 5.0) / 1023.0;
  windVoltage = (rawWind * 5.0) / 1023.0;
  
  // Keep the noise filter small so the turbine can work indoors
  if (windVoltage < 0.15) {
    windVoltage = 0.00;
  }
  
  totalVoltage = solarVoltage + windVoltage;
  
  // ☀️ MATCHING LOW PHYSICAL LED THRESHOLDS ☀️
  if (totalVoltage >= 0.8) {
    digitalWrite(LED_HOSPITAL, HIGH);
    digitalWrite(LED_RESIDENTIAL, HIGH);
    digitalWrite(LED_INDUSTRIAL, HIGH);
    digitalWrite(LED_COMMERCIAL, HIGH);
  }
  else if (totalVoltage >= 0.5) {
    digitalWrite(LED_HOSPITAL, HIGH);
    digitalWrite(LED_RESIDENTIAL, HIGH);
    digitalWrite(LED_INDUSTRIAL, HIGH);
    digitalWrite(LED_COMMERCIAL, LOW);
  }
  else if (totalVoltage >= 0.2) {
    digitalWrite(LED_HOSPITAL, HIGH);
    digitalWrite(LED_RESIDENTIAL, HIGH); // Your 0.34V will light this up instantly!
    digitalWrite(LED_INDUSTRIAL, LOW);
    digitalWrite(LED_COMMERCIAL, LOW);
  }
  else {
    digitalWrite(LED_HOSPITAL, HIGH);
    digitalWrite(LED_RESIDENTIAL, LOW);
    digitalWrite(LED_INDUSTRIAL, LOW);
    digitalWrite(LED_COMMERCIAL, LOW);
  }
  
  Serial.print("SOLAR:");
  Serial.print(solarVoltage, 2);
  Serial.print(",WIND:");
  Serial.print(windVoltage, 2);
  Serial.print(",TOTAL:");
  Serial.println(totalVoltage, 2);
  
  delay(500);
}