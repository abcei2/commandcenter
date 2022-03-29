# Importing Libraries
import serial
import time
import json
from flask import Flask, request
from firestore import Firestore
import http

sensorSerials = []
RESPONSE_TIMEOUT = 5

dbManager = Firestore("./serviceAccountKey.json")

def port_connected(port):   
    for sensorSerial in sensorSerials:
        if port == sensorSerial.port:
            return True, sensorSerial   

    try:
        aux_serial = serial.Serial(port=port, baudrate=9600, timeout=.1)     
        sensorSerials.append(aux_serial) 
        return True, aux_serial
    except serial.serialutil.SerialException:
        return False, None

def write_read(command):
    is_connected, arduino = port_connected(command["PORT"])

    if is_connected:
        print(type(command))
        arduino.write(bytes(json.dumps(command), 'utf-8'))
        time.sleep(0.5)
        data = arduino.readline()
        before = time.time()
        while data==b'' and time.time()< before + RESPONSE_TIMEOUT:        
            data = arduino.readline()
          

        if data !=b'':
            if data["ACK"]== "OK":
                if command["COMMAND"] == "ECREAD":
                    dbManager.savePPM(data["PPM"],data["TEMPERATURE"])
                elif command["COMMAND"] == "PHREAD":
                    dbManager.savePh(data["PH"])
            return data, 200
        else:
            return data, 500

    else:
        return "port doesn't exists", 404

app = Flask(__name__)

@app.route("/send_command", methods=['POST'])
def send_command():
    if request.method == 'POST':  
        return write_read(request.json)
    return "error"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
