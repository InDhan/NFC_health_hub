import serial.tools.list_ports
import time

def find_and_open_serial_port():
    # Get a list of available serial ports
    ports = serial.tools.list_ports.comports()

    # Iterate through the ports to find a suitable one
    for port in ports:
        if 'COM' in port.device:  # Adjust this condition as needed for your system
            try:
                # Attempt to open the serial port
                ser = serial.Serial(port.device, 9600)
                print(f"Opened serial port: {port.device}")
                return ser
            except serial.SerialException:
                continue
    
    # Return None if no suitable port is found
    return None

# Open the serial port using the find_and_open_serial_port() function
ser = find_and_open_serial_port()

# Check if the serial port is successfully opened
if ser is None:
    print("Error: No available serial port found!")
else:
    print("Serial port opened successfully.")

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
