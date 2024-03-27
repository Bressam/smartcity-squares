# Smart City: Squares
Smart city study project for smart squares monitoring.
Project uses ESP32 and communicate remotely for IoE using MQTT protocol.
Language used was uPython.

## ESP32 Simulator:
 - Code can be either run on a ESP32 device or emulated through [Wokwi platform](https://wokwi.com/).

## System Overview:
 - The system can be simplified to 3 main parts: 
   - ESP32 as IoT device;
   - HiveMQ as MQTT Broker platform, to listen and publish data;
   - Node-RED platform for dashboard and visualization of MQTT collected data;
<img width=720px src="https://github.com/Bressam/smartcity-squares/blob/main/SampleResources/system_overview.png">
