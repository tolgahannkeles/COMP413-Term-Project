# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import socket
import json
import urequests
import time

# Firestore REST API URL for updating documents
FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/iot-project-db90a/databases/(default)/documents/gateway_data"

# WiFi access point configuration
AP_SSID = "GatewayHotspot"  # The name of your Wi-Fi hotspot
AP_PASSWORD = "password123"  # The password for the Wi-Fi hotspot
AP_IP = "192.168.4.1"  # The IP address for the gateway in AP mode
SERVER_PORT = 8081  # Listening UDP port

# External WiFi network configuration (for internet access)
EXTERNAL_WIFI_SSID = "IOT_03"  # The SSID of the external Wi-Fi network
EXTERNAL_WIFI_PASSWORD = "test0303"  # The password for the external Wi-Fi network

# Function to create a Wi-Fi access point
def create_ap(ssid, password):
    try:
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA2_PSK)

        while not ap.active():
            time.sleep(1)
        
        print(f"Access Point '{ssid}' created with IP address {ap.ifconfig()[0]}")
    except Exception as e:
        print("Error creating access point:", e)

# Function to connect to external Wi-Fi network (STA mode)
def connect_to_external_wifi(ssid, password):
    try:
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        sta.connect(ssid, password)
        
        # Wait for connection
        while not sta.isconnected():
            print("Connecting to external Wi-Fi...")
            time.sleep(1)
        
        print("Connected to external Wi-Fi!")
        print("IP Address:", sta.ifconfig()[0])
    except Exception as e:
        print("Error connecting to external Wi-Fi:", e)

# Function to send data to Firestore REST API
def update_firestore(parking_id, data):
    try:
        # Construct Firestore document URL using parking_id as the document ID
        firestore_doc_url = f"{FIRESTORE_URL}/{parking_id}"
        
        # Prepare Firestore update payload
        firestore_payload = {
            "fields": {
                "status": {"integerValue": data["status"]} if data.get("status") is not None else {"nullValue": None},
                "distance": {"doubleValue": data["distance"]} if data.get("distance") is not None else {"nullValue": None},
                "latitude": {"doubleValue": data["latitude"]} if data.get("latitude") is not None else {"nullValue": None},
                "longitude": {"doubleValue": data["longitude"]} if data.get("longitude") is not None else {"nullValue": None}
            }
        }

        # Send PATCH request to update the document
        response = urequests.patch(
            firestore_doc_url,
            json=firestore_payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"Response from Firestore: {response.text}")
        response.close()
        print(f"Data for ID {parking_id} sent to Firestore.")

    except Exception as e:
        print("Error updating document:", e)

# UDP socket setup for the AP
def start_udp_server():
    print("Starting UDP server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((AP_IP, SERVER_PORT))
    print(f"Gateway listening on {AP_IP}:{SERVER_PORT}...")

    try:
        while True:
            # Receive UDP packet
            data, addr = server_socket.recvfrom(1024)
            try:
                decoded_data = json.loads(data.decode())
                parking_id = decoded_data["id"]
                update_firestore(parking_id, decoded_data)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON data received: {data.decode()}")
            except KeyError as e:
                print(f"Missing key in received data: {e}")

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # Create Wi-Fi Access Point (GatewayHotspot)
    create_ap(AP_SSID, AP_PASSWORD)

    # Connect to external Wi-Fi for internet access
    connect_to_external_wifi(EXTERNAL_WIFI_SSID, EXTERNAL_WIFI_PASSWORD)

    # Start UDP server to listen for data from clients
    start_udp_server()

