#define WATER_SENSOR 8  // Mendefinisikan pin WATER_SENSOR sebagai pin 8

void setup()
{
  Serial.begin(9600);  // Memulai komunikasi serial dengan baud rate 9600
  pinMode(WATER_SENSOR, INPUT);  // Mengatur pin WATER_SENSOR sebagai input
}

void loop()
{
  int sensorValue = digitalRead(WATER_SENSOR);  // Membaca nilai sensor pada pin WATER_SENSOR
  
  if (sensorValue == 0) {  // Jika nilai sensor adalah 0 (basah)
    Serial.println("Basah");  // Mencetak "Basah" ke Serial Monitor
  } else {  // Jika nilai sensor bukan 0 (kering)
    Serial.println("Aman");  // Mencetak "Aman" ke Serial Monitor
  }
  
  delay(500);  // Delay selama 500 milidetik
}
