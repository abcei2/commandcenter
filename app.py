# Importing Libraries
import serial
import time
import json
from flask import Flask, request

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.5)
    data = arduino.readline()
    while data==b'':
        data = arduino.readline()
    print(data)
    return data

app = Flask(__name__)

@app.route("/send_command", methods=['POST'])
def send_command():
    if request.method == 'POST':
        
        command = {
            "COMMAND":request.form['COMMAND']
        }
        return write_read(json.dumps(command))
    return "error"

@app.route("/ecread")
def ecread():
    command = {
        "COMMAND":"ECREAD"  
    }
    return write_read(json.dumps(command))

@app.route("/ecup")
def ecup():
    command = {
        "COMMAND":"ECUP"  
    }
    return write_read(json.dumps(command))
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
