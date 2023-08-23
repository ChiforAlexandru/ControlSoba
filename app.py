#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
from time import sleep
import sys

app = Flask(__name__)
CORS(app)

motor_channel = (29,31,33,35)
temp_channel = (3)

def move_motor_gpio(di):
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motor_channel, GPIO.OUT)
    if(di == 1):
        seq = [(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH),
                (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH),
                (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
                (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW)]
    else:
        seq = [(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH),
                (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW),
                (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
                (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)]
    for i in range(80):
        GPIO.output(motor_channel,  seq[i % 4])
        sleep(0.02)
    GPIO.cleanup()
    del GPIO

def read_temp_humidity():
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    import adafruit_dht
    import psutil
    import board
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(11, GPIO.IN)
    sleep(0.1)
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()
    sleep(0.1)
    sensor=adafruit_dht.DHT11(board.D17) 
    res={ 'temperature':0, 'humidity':0 }
    sleep(0.1)
    try:
        res['temperature']=sensor.temperature
        sleep(0.1)
        res['humidity']=sensor.humidity
        sleep(0.1)
  
    except RuntimeError as error:
        sensor.exit() 
        del adafruit_dht
        del psutil
        del board
        GPIO.cleanup()  
        del GPIO
        return error.args[0]
    except Exception as error:
        sensor.exit() 
        del adafruit_dht
        del psutil
        del board
        GPIO.cleanup()  
        del GPIO
        raise error
    sensor.exit()  
    sleep(0.1)
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()
    sleep(0.1)
    del adafruit_dht
    del psutil
    del board
    GPIO.cleanup()  
    del GPIO
    return res

def read_carbon():
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    import board
    import busio
    import adafruit_ads1x15.ads1015 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

    i2c=busio.I2C(board.SCL, board.SDA)
    ads=ADS.ADS1015(i2c)
    ads.gain=1
    chan=AnalogIn(ads, ADS.P0)
    del board
    del busio
    del ADS
    del AnalogIn
    GPIO.cleanup()  
    del GPIO
    rt=chan.value//1000
    if rt<100:
        rts=str(rt)+"ppm (Nivel normal)"
    elif rt>99 and rt<150:
        rts=str(rt)+"ppm (Se recomandă aerisirea spațiului)"
    else:
        rts=str(rt)+"ppm (Nivel periculos)"
    return rts

@app.route('/api/v1.0/temp', methods=['GET'])
def get_temp():
    r=read_temp_humidity()
    return jsonify(r)

@app.route('/api/v1.0/carbon', methods=['GET'])
def get_carbon():
    rc=read_carbon()
    return jsonify(rc)

@app.route('/api/v1.0/motor', methods=['GET'])
def move_motor():
    move_motor_gpio(0)
    return jsonify({'message': 'Succes'})

@app.route('/api/v1.0/motor-l', methods=['GET'])
def move_motor_l():
    move_motor_gpio(1)
    return jsonify({'message': 'Succes'})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000, debug=True)
