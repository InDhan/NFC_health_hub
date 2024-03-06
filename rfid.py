from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_rfid_id():
    id, text = reader.read()
    
    return id

def read_rfid_string():
    id, text = reader.read()
    return text

def write_rfid():
    text = str(input("enter the new patient id "))
    id, text_written = reader.write(text)
    print(f"ID: {id}")
    print(f"Text Written succesfully : {text_written}")

if __name__ == '__main__':
   rfid_id = read_rfid_id()
   patient_id = read_rfid_string()
   print(f'your id is at {rfid_id} and your patient_id is {patient_id}')