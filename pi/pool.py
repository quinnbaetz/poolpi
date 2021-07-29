
#!/usr/bin/python
import spidev
import RPi.GPIO as GPIO 
import time
from flask import Flask
from w1thermsensor import W1ThermSensor, Sensor, Unit

GPIO.setmode(GPIO.BCM)
SWITCH_PIN=22
GPIO.setup(SWITCH_PIN, GPIO.IN)
DIFFERENCE_TO_CHANGE = 5

waterSensor = W1ThermSensor(sensor_id="01192111db9e")
solarSensor = W1ThermSensor(sensor_id="01191a4f861a")
spi = spidev.SpiDev()
FILENAME='temp.txt'
WATER_SPI = 0
SOLAR_SPI = 1
solarOn = True

f = open(FILENAME, "r")
preferredTemp = f.read())
f.close()


def waterTemp()
    waterTemp = waterSensor.get_temperature(Unit.DEGREES_F)
    solarTemp = solarSensor.get_temperature(Unit.DEGREES_F)
    print("The temperature is %s, %s" % (waterTemp, solarTemp))
    time.sleep(5)

def writePot(input, type):
    spi.open(0, type)
    spi.max_speed_hz = 976000
    msb = input >> 8
    lsb = input & 0xFF
    spi.xfer([msb, lsb])

def turnOnSolar():
    solarOn = True
    writePot(0, 0)
    writePot(130, 1)
    
def turnOffSolar():
    solarOn = False
    writePot(130, 0)
    writePot(0, 1)

def writeSolarResistance(resistance)
    writePot(resistance, SOLAR_SPI)

def writeWaterResistance(resistance)
    writePot(resistance, WATER_SPI)


LOW = 0
HIGH = 130
def tempToResistanceOutput(temp):
  ohms = 46019.35 - 680.9114*temp + 2.781725*temp*temp
  unvalidated_output = -0.01322926*ohms + 192.2938
  return max(LOW, min(HIGH, unvalidated_output))


def checkOnSensors():
  ignoreTempValue = GPIO.input(SWITCH_PIN)
  waterTemp = waterSensor.get_temperature(Unit.DEGREES_F)
  solarTemp = solarSensor.get_temperature(Unit.DEGREES_F)
  print("The temperature is %s, %s" % (waterTemp, solarTemp))
  if ignoreTempValue:
    waterOutput = tempToResistanceOutput(waterTemp)
    writeWaterResistance(waterOutput)
    solarOutput = tempToResistanceOutput(solarTemp)
    writeSolarResistance(waterOutput)
  else:
    if waterTemp < preferredTemp and !solarOn:
      turnOnSolar()
    elif waterTemp + DIFFERENCE_TO_CHANGE > preferredTemp and solarOn:
      turnOffSolar()
      

app = Flask(__name__)

@app.route('/')
def index():
    return 'Things are working and you have access'

@app.route('/temperature', methods = ['POST'])
def temperature(temp):
    if request.method == 'GET':
        return temp
    if request.method == 'POST':
        tempParam = request.form.get("temp")
        f = open(FILENAME, "w")
        f.write(int(tempParam))
        preferredTemp = tempParam
        f.close()
        checkOnSensors()
        return preferredTemp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

turnOnSolar()


while True:
    checkOnSensors()    
    time.sleep(600)
