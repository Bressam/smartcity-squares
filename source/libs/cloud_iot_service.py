from umqttsimple import MQTTClient
import wifi_utils

class CloudIOTService:
    # Initial setup
    def __init__(self, mqttDefaultConfig, mqttSubscription, callback):
        self.mqttDefaultConfig = mqttDefaultConfig
        self.setupConnection()

        # Setup callbacks and listener
        self.setCallBack(callback)
        self.subscribeTo(mqttSubscription)
    
    # Setup WLANClient and MQTTClient
    def setupConnection(self):
        # Wokwi virtual SSID and password
        wifiSSID = "Wokwi-GUEST"
        wifiPassword = ""

        # Start connection
        print("Connecting...")
        self.wlanStation = wifi_utils.createWLANStation(wifiSSID, wifiPassword)
        if not self.wlanStation.isconnected():
            print("ERROR: Wi-Fi connection failed")
        else:
            print("Wi-Fi connected")
            print("Connecting to MQTT Broker...")
            client = MQTTClient(
                self.mqttDefaultConfig.mqtt_client_id,
                self.mqttDefaultConfig.mqtt_server,
                self.mqttDefaultConfig.mqtt_port,
                self.mqttDefaultConfig.mqtt_user,
                self.mqttDefaultConfig.mqtt_password)
            client.connect()
            self.mqttClient = client
            print("Connected sucessfully to MQTT Broker!")
            return self.wlanStation, self.mqttClient
    
    # API Communication with MQQT Broker
    def sendManualControlState(self, isOn):
        controlString = "ON" if isOn else "OFF" 
        self.mqttClient.publish("bressam/nodered/sprinkler/manualcontrol", controlString)
    
    def sendHumidity(self, humidityPercentageStr):
        self.mqttClient.publish("bressam/nodered/humidity", humidityPercentageStr)

    def sendSprinklerState(self, sprinklerStateStr):
        self.mqttClient.publish("bressam/nodered/sprinkler", sprinklerStateStr)

    def sendSprinklerPercentage(self, sprinklerServoAngleStr):
        self.mqttClient.publish("bressam/nodered/sprinkler/angle", sprinklerServoAngleStr)
    
    def setCallBack(self, callback):
        self.mqttClient.set_callback(callback)
    
    def subscribeTo(self, topicMQTT):
        self.mqttClient.subscribe(topicMQTT)
    
    # Not really a sleep, its waiting for 1s calling check_msg each 0.1s
    def listenSubscriptionFor(self, seconds):
        self.mqttClient.sleep(seconds)