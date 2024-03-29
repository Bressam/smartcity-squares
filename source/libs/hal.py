from machine import Pin
from servo import Servo
import dht
import time

class Hal:
    #Pins
    sprinklerLedIndicator = Pin(5, Pin.OUT)
    servo = Servo(2)
    dhtPin = Pin(22, Pin.IN)
    dht22 = dht.DHT22(dhtPin)
    humidityPercentage = 0
    isLoading = False

    # Initial setup and readings
    def __init__(self):
        self.dht22.measure()
        self.humidityPercentage = self.dht22.humidity()
        self.setSprinklersTo(False)
        print("Sprinklers Off. Initial humidity reading: ", self.humidityPercentage)

    def toggleConnectionLed(self):
        if self.getLedValue() == 0:
            self.setLedOn()
        else:
            self.setLedOff()

    # HAL Pins communication
    def updateLoadingIndication(self):
        while self.isLoading:
            self.toggleConnectionLed()
            time.sleep(0.5)

    # HAL API
    def perfomSensorReading(self):
        self.dht22.measure()
        self.humidityPercentage = self.dht22.humidity()

    def setLoadingIndicationTo(self, isLoading):
        self.isLoading = isLoading
        self.updateLoadingIndication()
    
    def setLedOn(self):
        self.sprinklerLedIndicator.on()
    
    def setLedOff(self):
        self.sprinklerLedIndicator.off()
    
    def setServoAngle(self, servoAngleInt):
        if servoAngleInt >= 0 and servoAngleInt <= 180:
            self.servo.set_angle(servoAngleInt)
    
    def getHumidityValue(self):
        return self.humidityPercentage
    
    def getLedValue(self):
        return self.sprinklerLedIndicator.value()

    def setSprinklersTo(self, isOn):
        if isOn:
            self.setServoAngle(180)
            self.setLedOn()
        else:
            self.setServoAngle(0)
            self.setLedOff()
    
    def getSprinklerAngle(self):
        return self.servo.angle