import wifi_utils
import time
from mqtt_config import MqttDefaultConfig
from umqttsimple import MQTTClient
from hal import Hal
import _thread


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
    print(topic)
    print(msg)

    # LED Control
    if msg.decode() == "ON" or msg.decode() == "OFF":
        if msg.decode() == "ON":
            hal.setLedOn()
        if msg.decode() == "OFF":
            hal.setLedOff()
    # Sprinkler control
    else:
        servoAngle = msg.decode()
        if servoAngle.isdigit():
            print(servoAngle)
            print(type(servoAngle))
            servoAngleInt = int(servoAngle)
            print(servoAngleInt)
            print(type(servoAngleInt))
            hal.setServoAngle(servoAngleInt)
            # if servoAngle > 0 and servoAngle <= 180:
            #     servo.set_angle(servoAngle)
    
    updateDashBoard()

# Send data do update node-red MQQT listener
def updateDashBoard():
    global hal
    mqttClient.publish("bressam/nodered/led", str(hal.getLedValue()))
    mqttClient.publish("bressam/nodered/humidity", str(hal.getHumidityValue()))

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
mqttClient.set_callback(responseReceived)
mqttClient.subscribe("bressam/esp32client")

while True:
    print("Sending data: ")
    updateDashBoard()
    # Not really a sleep, its waiting for 1s calling check_msg each 0.1s
    mqttClient.sleep(1)

#publish test
#mqttClient.publish("bressam/testtopic", "connected")
#time.sleep(1)

mqttClient.disconnect()
wlanStation.disconnect()