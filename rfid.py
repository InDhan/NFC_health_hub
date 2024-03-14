from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_rfid():
    id, text = reader.read()
    print(f"ID: {id}")
    print(f"Text: {text}")
    return text

def write_rfid():
    text = str(input("enter the new patient id "))
    id, text_written = reader.write(text)
    print(f"ID: {id}")
    print(f"Text Written succesfully : {text_written}")