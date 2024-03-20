import serial
import time

# Define the serial port and baud rate
ser = serial.Serial('COM6', 9600)  # Adjust COM port as needed

def read_rfid():
    while True:
        # Read data from the Arduino
        data = ser.readline().strip().decode('utf-8')
        if data:
            return data

if __name__ == '__main__':
    try:
        while True:
            uid = read_rfid()
            print("RFID Tag UID:", uid)
            time.sleep(1)  # Delay for readability
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()  # Close the serial port
