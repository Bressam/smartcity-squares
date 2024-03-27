from wifi_lib import conecta
import urequests
import time
from umqttsimple import MQTTClient

wifiSSID = "Wokwi-GUEST"
wifiPassword = ""
mqtt_server = "broker.mqttdashboard.com"
mqtt_port = 1883
mqtt_user = ""
mqtt_password = ""
mqtt_client_id = "client-id-bressam-YfdodFe"

print("Conectando...")
station = conecta(wifiSSID, wifiPassword)
if not station.isconnected():
    print("Falha na conexão Wi-Fi")
else:
    print("Conectado wifi")
    print("Conectando Broker MQTT")
    client = MQTTClient(mqtt_client_id,
        mqtt_server,
        mqtt_port,
        mqtt_user,
        mqtt_password)
    client.connect()
    
    print("MQTT Conectado!")

    client.publish("bressam/testtopic", "123.134")
    time.sleep(1)
    client.disconnect()
    station.disconnect()
