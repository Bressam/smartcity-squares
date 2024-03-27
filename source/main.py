import wifi_utils
import time
from mqtt_config import MqttDefaultConfig
from umqttsimple import MQTTClient

# Checks if needed connections are setup
def checkSetupSuccessfully(mqttClient, wlanStation):
    return type(mqttClient) is not None and type(wlanStation) is not None

# Initial setup: organize console prints, try to create clients and check if they are setup correctly
def setup():
    # Clean terminal logs
    for i in range(0, 10):
        print("\n")

    wlanStation, mqttClient = setupConnection()
    if not checkSetupSuccessfully(mqttClient, wlanStation):
        print("ERROR: Failed to setup connections. Terminating code, disconnecting clients if any exists.")
        if type(mqttClient) is not None:
            mqttClient.disconnect()
        if type(wlanStation) is not None:
            wlanStation.disconnect()
    else:
        return wlanStation, mqttClient

def responseReceived(topic, msg):
    print(topic)
    print(msg)

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
wlanStation, mqttClient = setup()
mqttClient.set_callback(responseReceived)
mqttClient.subscribe("bressam/esp32client")

print("Waiting for responses")
for i in range(60):
    mqttClient.check_msg()
    time.sleep(1)

#publish test
#mqttClient.publish("bressam/testtopic", "connected")
#time.sleep(1)

mqttClient.disconnect()
wlanStation.disconnect()
