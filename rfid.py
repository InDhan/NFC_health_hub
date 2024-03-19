from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    while True:
        # Wait for the RFID tag to be scanned
        print("Hold a tag near the reader")
        id, text = reader.read()

        # Print the ID and data of the scanned tag
        print("Tag ID: {}".format(id))
        print("Tag Data: {}".format(text))

finally:
    # Cleanup the RFID reader
    GPIO.cleanup()
