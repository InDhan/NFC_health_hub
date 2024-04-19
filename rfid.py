import serial
import sys

def read_rfid():
    ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Adjust port as necessary

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('latin-1').strip()  # Try decoding with 'latin-1'
                return line
    except KeyboardInterrupt:
        ser.close()
        print("Program terminated")

if __name__ == "__main__":
    try:
        print("Waiting for RFID data...")
        while True:
            patient_id = read_rfid()
            print("RFID data received:", patient_id)
    except Exception as e:
        print("Error:", e)
