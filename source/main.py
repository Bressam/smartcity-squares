import time
from mqtt_config import MqttDefaultConfig
from hal import Hal
from cloud_iot_service import CloudIOTService
import _thread

version = 1.000.000

# Variables
enableMQTTDebugPrint = True
isUnderManualControl = False


def responseReceived(topic, msg):
    global hal
    global isUnderManualControl
    
    if enableMQTTDebugPrint: print("Received msg: ", msg, "From topic: ", topic)

    # Manual sprinkler control
    if msg.decode() == "ON" or msg.decode() == "OFF":
        if msg.decode() == "ON":
            hal.setSprinklersTo(True)
            updateDashBoard()
            isUnderManualControl = True
        if msg.decode() == "OFF":
            isUnderManualControl = False
            hal.setSprinklersTo(False)
    # Sprinkler strength control. Only available under manual control
    else:
        if not isUnderManualControl: return
        servoAngle = msg.decode()
        if servoAngle.isdigit():
            servoAngleInt = int(servoAngle)
            hal.setServoAngle(servoAngleInt)

# Send data do update node-red MQQT listener
def updateDashBoard():
    global isUnderManualControl
    global hal
    sprinklerSystemStateStr = str(hal.getLedValue())
    humidityValueStr = str(hal.getHumidityValue())
    print("Sending data: ", " Humidity: ", humidityValueStr, "Sprinkler state: ", sprinklerSystemStateStr)
    cloudIOTService.sendHumidity(humidityValueStr)
    cloudIOTService.sendSprinklerState(sprinklerSystemStateStr)

    if not isUnderManualControl:
        sprinklerServoAngleStr = str(hal.getSprinklerAngle())
        print("Sending sprinkler servo angle: ", sprinklerServoAngleStr)
        cloudIOTService.sendSprinklerPercentage(sprinklerServoAngleStr)

# Checks if needed connections are setup
def checkSetupSuccessfully(mqttClient, wlanStation):
    return type(mqttClient) is not None and type(wlanStation) is not None

# Initial setup: organize console prints, try to create clients and check if they are setup correctly
def setup():
    # Clean terminal logs
    for i in range(0, 10):
        print("\n")
    
    hal = Hal()
    cloudIOTService = CloudIOTService(MqttDefaultConfig(), "bressam/esp32client", responseReceived)
    if not checkSetupSuccessfully(cloudIOTService.mqttClient, cloudIOTService.wlanStation):
        print("ERROR: Failed to setup connections. Terminating code, disconnecting clients if any exists.")
        if type(mqttClient) is not None:
            mqttClient.disconnect()
        if type(wlanStation) is not None:
            wlanStation.disconnect()
    else:
        return hal, cloudIOTService


# Sprinkler control based on humidity level
def activateSprinklerIfNeeded():
    global isUnderManualControl
    if isUnderManualControl: return

    global hal
    humidityPercentage = hal.getHumidityValue()
    # Low humidity, turn sprinklers until safe level reached
    print(humidityPercentage)
    if humidityPercentage <= 30:
        hal.setSprinklersTo(True)
    elif humidityPercentage >= 60:
        hal.setSprinklersTo(False)

## Main
hal, cloudIOTService = setup()
# Start syncing manual to off to remote control
cloudIOTService.sendManualControlState(False)

# Main loop
while True:
    hal.perfomSensorReading()
    activateSprinklerIfNeeded()
    updateDashBoard()
    cloudIOTService.listenSubscriptionFor(1)
