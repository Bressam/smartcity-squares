import wifi_utils
import time
from mqtt_config import MqttDefaultConfig
from umqttsimple import MQTTClient
from hal import Hal
import _thread

enableMQTTDebugPrint = True
isUnderManualControl = False

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


# Checks if needed connections are setup
def checkSetupSuccessfully(mqttClient, wlanStation):
    return type(mqttClient) is not None and type(wlanStation) is not None

# Initial setup: organize console prints, try to create clients and check if they are setup correctly
def setup():
    # Clean terminal logs
    for i in range(0, 10):
        print("\n")
    
    hal = Hal()
    # hal.setLoadingIndicationTo(True)
    wlanStation, mqttClient = setupConnection()
    if not checkSetupSuccessfully(mqttClient, wlanStation):
        print("ERROR: Failed to setup connections. Terminating code, disconnecting clients if any exists.")
        hal.setLoadingIndicationTo(False)
        if type(mqttClient) is not None:
            mqttClient.disconnect()
        if type(wlanStation) is not None:
            wlanStation.disconnect()
    else:
        hal.setLoadingIndicationTo(False)
        return wlanStation, mqttClient

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
    mqttClient.publish("bressam/nodered/sprinkler", sprinklerSystemStateStr)
    mqttClient.publish("bressam/nodered/humidity", humidityValueStr)

    if not isUnderManualControl:
        sprinklerAngleStr = str(hal.getSprinklerAngle())
        print("Sending Sprinkler angle: ", sprinklerAngleStr)
        mqttClient.publish("bressam/nodered/sprinkler/angle", sprinklerAngleStr)

# Setup WLANClient and MQTTClient
def setupConnection():
    # Wokwi virtual SSID and password
    wifiSSID = "Wokwi-GUEST"
    wifiPassword = ""
    mqttDefaultConfig = MqttDefaultConfig()

    # Start connection
    print("Connecting...")
    wlanStation = wifi_utils.createWLANStation(wifiSSID, wifiPassword)
    if not wlanStation.isconnected():
        print("ERROR: Wi-Fi connection failed")
    else:
        print("Wi-Fi connected")
        print("Connecting to MQTT Broker...")
        client = MQTTClient(
            mqttDefaultConfig.mqtt_client_id,
            mqttDefaultConfig.mqtt_server,
            mqttDefaultConfig.mqtt_port,
            mqttDefaultConfig.mqtt_user,
            mqttDefaultConfig.mqtt_password)
        client.connect()
        mqttClient = client
        print("Connected sucessfully to MQTT Broker!")
        return wlanStation, mqttClient


# Send data through connection setup
hal = Hal()
wlanStation, mqttClient = setup()
# Start syncing manual to off to remote control
mqttClient.publish("bressam/nodered/sprinkler/manualcontrol", "OFF")

# Setup callbacks and listener
mqttClient.set_callback(responseReceived)
mqttClient.subscribe("bressam/esp32client")

# Main loop
while True:
    hal.perfomSensorReading()
    activateSprinklerIfNeeded()
    updateDashBoard()
    # Not really a sleep, its waiting for 1s calling check_msg each 0.1s
    mqttClient.sleep(1)