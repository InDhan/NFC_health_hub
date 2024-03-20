import pandas as pd 
import serial 
import time

dataobj = serial.Serial('com3')
time.sleep(1)

def read_data():
     print("Waiting RFID module for connection............")
     while True:
       while (dataobj.in_waiting()==0):
        pass
       rfid_text = dataobj.readline()
       rfid_text = int(patient_id,'int64')
    
     return rfid_text 

def write_data():
   pass

patient_id = read_data()
print(patient_id)