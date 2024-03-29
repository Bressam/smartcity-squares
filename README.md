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
<img width=720px src="https://github.com/Bressam/smartcity-squares/blob/main/SampleResources/system_overview_colors.png">

## Project objective
- The main objective is that the system measures constantly the earth humidity of each sqaure sub division, and if detected low humidity at that division of the square it automatically turns on the sprinklers system and also a light for indication;
- The system constantly update data remotely to a dashboard (image below), making possible 2 things:
    - Remotely checking values measured (ground humidity and percentage of water flow at sprinklers) and if system is active or not;
    - Remotely triggering a manual activation of the sprinkle system;

<img width=720px src="https://github.com/Bressam/smartcity-squares/blob/main/SampleResources/dashboard.png">


- The light indicator of the area with sprinklers on can be either on illumination poles or into a more complex system inside small water fountains as demonstrated below:

| Light poles (purple for system active)  | Ware Foutains (purple for system active) |
| -------------|-------------|
| <img width=360px src="https://github.com/Bressam/smartcity-squares/blob/main/SampleResources/1.png">|<img width=360px src="https://github.com/Bressam/smartcity-squares/blob/main/SampleResources/2.png">|


