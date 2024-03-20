#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9  // Define the RST_PIN (reset pin) for the RC522 module
#define SS_PIN 10  // Define the SS_PIN (slave select pin) for the RC522 module

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  
  SPI.begin();  // Initialize SPI communication
  mfrc522.PCD_Init();  // Initialize MFRC522 module
  
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

    // Write data to the card (if needed)
    byte data[] = {0xDE, 0xAD, 0xBE, 0xEF};  // Example data to write
    MFRC522::StatusCode status = mfrc522.MIFARE_Write(1, data, sizeof(data));
    if (status == MFRC522::STATUS_OK) {
      Serial.println("Data written to card");
    } else {
      Serial.println("Error writing data to card");
    }

    delay(1000);  // Delay for readability
  }
}
