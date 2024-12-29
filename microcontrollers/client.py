import socket
import time
import random
import json
import network
from hcsr04 import HCSR04
from machine import Pin


# Wi-Fi bağlantısı
SSID = "GatewayHotspot"  # Wi-Fi ağ adı
PASSWORD = "password123"  # Wi-Fi şifresi

# Server bilgileri
SERVER_IP = "192.168.4.1"  # Sunucunun IP adresi
SERVER_PORT = 8081  # Sunucunun dinlediği UDP portu
THRESHOLD = 15
ID = 1

led= Pin(2, Pin.OUT)


# Park status replacements
PARK_STATUS = {
    "FULL": 1,
    "EMPTY": 0,
    "UNKNOWN": -1,
}

"""
    Requirements for the client:
    1. Send data to the gateway when the state of the parking lot changes.
    2. The data to be sent must be in JSON format.
    3. The data to be sent must contain the following fields:
        - id: The ID of the parking lot.
        - distance: The distance to the parking lot.
        - status: The status of the parking lot. 0: Not available, 1: Available
    4. The client should send the alive message to the gateway every 5 seconds.
"""

data_dict = {
    "id": ID,
    "distance": 0,
    "status": PARK_STATUS["UNKNOWN"],
    "latitude":38.737177, 
    "longitude":35.472940
}

def connect_to_wifi():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print("Wi-Fi'ye bağlanılıyor...")
            wlan.connect(SSID, PASSWORD)
            led.on()
            while not wlan.isconnected():
                led.off()
                pass
            led.on()
        print("Bağlandı:", wlan.ifconfig())
    except Exception as e:
        print("Wi-Fi bağlantısı yapılamadı:", e)

def is_threshold_passed(value):
    return value > THRESHOLD

def get_distance():
    return distance_sensor.distance_cm()

def get_park_status():
    try:
        distance = get_distance()
        print(distance)
        data_dict["distance"] = distance  # Mesafeyi JSON'a ekle
        if is_threshold_passed(distance):
            return "EMPTY"
        return "FULL"
    except Exception as e:
        print("Error: ", e)
        return "UNKNOWN"

def send_to_server(status):
    if status in PARK_STATUS:
        data_dict["status"] = PARK_STATUS[status]
        client_socket.sendto(json.dumps(data_dict).encode(), (SERVER_IP, SERVER_PORT))
    else:
        raise ValueError("Invalid value for status")

prev_status = "EMPTY"

# UDP soketi oluştur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
distance_sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

try:
    connect_to_wifi()  # Wi-Fi bağlantısını kur
    print("Veri gönderimi başlıyor...")
    while True:
        current_status = get_park_status()
        print("Current status: ", current_status, " Previous Status: ", prev_status)
        if current_status != prev_status:
            print("Veri gönderiliyor...")
            send_to_server(current_status)
            prev_status = current_status
        # 5 saniye bekle
        time.sleep(5)
except KeyboardInterrupt:
    print("\nVeri gönderimi durduruldu.")
finally:
    client_socket.close()




