import serial.tools.list_ports
import time
previous RFID UIser = None  # Initialize serial port variable
rfid_uid = None  # Initialize RFID UID variable

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

def read_rfid():
    global ser, rfid_uid
    while True:
        if ser is not None and ser.is_open:
            # Read data from the Arduino
            data = ser.readline().strip().decode('utf-8')
            if data:
                rfid_uid = data
                print("Patient RFID:", rfid_uid)
        time.sleep(0.1)  # Adjust delay as needed

def start_rfid_thread():
    global ser
    ser = find_and_open_serial_port()
    if ser is None:
        print("Error: No available serial port found!")
    else:
        print("Serial port opened successfully.")
        # Start a new thread to run the RFID reader function
        rfid_thread = threading.Thread(target=read_rfid)
        rfid_thread.daemon = True
        rfid_thread.start()

# Variable to store theD
prev_rfid_uid = None


if __name__ == '__main__':
    start_rfid_thread()
    try:
        while find_and_open_serial_port() != None:
            uid = read_rfid()
            print("RFID Tag UID:", uid)
            time.sleep(1)  # Delay for readability
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()  # Close the serial port
