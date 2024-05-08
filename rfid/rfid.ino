#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9  // Define the RST_PIN (reset pin) for the RC522 module
#define SS_PIN 10  // Define the SS_PIN (slave select pin) for the RC522 module
#define LED_PIN 8  // Define the LED_PIN for the LED

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  
  SPI.begin();  // Initialize SPI communication
  mfrc522.PCD_Init();  // Initialize MFRC522 module

  pinMode(LED_PIN, OUTPUT);  // Set LED_PIN as output
  
  Serial.println("MFRC522 Initialized");
}

void loop() {
  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    // Print UID of the card
    Serial.print("UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
      Serial.print(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println();

    digitalWrite(LED_PIN, HIGH);  // Turn on the LED
    delay(1000);  // Delay for readability
    digitalWrite(LED_PIN, LOW);  // Turn off the LED
  }
}
