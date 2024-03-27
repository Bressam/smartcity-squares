import network
import time

def createWLANStation(ssid, senha, shouldPrintLoad = True):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, senha)
    for t in range(500):
        if station.isconnected():
            print("")
            break
        time.sleep(0.1)
        if shouldPrintLoad:
            print(".", end="")
    return station
