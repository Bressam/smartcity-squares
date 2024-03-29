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
        print("Initial humidity reading: ", self.humidityPercentage)

    def toggleConnectionLed(self):
        if self.sprinklerLedIndicator.value() == 0:
            self.sprinklerLedIndicator.on()
        else:
            self.sprinklerLedIndicator.off()

    # HAL Pins communication
    def updateLoadingIndication(self):
        while self.isLoading:
            self.toggleConnectionLed()
            time.sleep(0.5)

    # HAL API
    def setLoadingIndicationTo(self, isLoading):
        print("Set loading to: ", isLoading)
        self.isLoading = isLoading
        self.updateLoadingIndication()
    
    def setLedOn(self):
        self.connectionIndicator.on()
    
    def setLedOff(self):
        self.connectionIndicator.off()
    
    def setServoAngle(self, servoAngleInt):
        if servoAngleInt >= 0 and servoAngleInt <= 180:
            self.servo.set_angle(servoAngleInt)
    
    def getHumidityValue(self):
        return humidityPercentage
    
    def getLedValue(self):
        return self.sprinklerLedIndicator.value()
