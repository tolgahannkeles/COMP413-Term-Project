# COMP413-G5-Smart-Parking-System

## Project Overview
The **Smart Parking System** is an IoT-based solution aimed at addressing the inefficiencies in parking management in urban areas. By reducing the time and effort required to locate parking spots, the system minimizes traffic congestion, fuel consumption, and environmental damage. The system uses ultrasonic sensors and ESP32 microcontrollers to detect and relay parking space availability to users in real time via a mobile application and web dashboard.

---

## Problem Statement
In cities, inefficient use of parking spaces contributes significantly to traffic congestion and environmental harm. Drivers waste time and fuel searching for available parking spots, increasing air pollution and stress. This project aims to create a smart, scalable solution to optimize parking management using IoT technologies.

---

## System Architecture

### **Sensing Layer**
- **Components**: Ultrasonic sensors (3x HCSR04), ESP32 (2x) and ESP32S Mini (1x).
- **Functionality**: Detects the presence or absence of vehicles based on distance measurements. Sends data to the gateway only when there is a state change (e.g., from `empty` to `full`).

### **Communication Layer**
- **Components**: ESP32S Mini (Gateway).
- **Functionality**: Receives data from sensor nodes and forwards it to Firebase for storage and real-time updates.

### **Application Layer**
- **Components**: Flutter-based mobile application, Firebase backend.
- **Functionality**: Retrieves data from Firebase and displays parking space availability on an interactive map.

---

## Hardware Design
### Components Used
1. **Ultrasonic Sensors (HCSR04)**:
   - Measures the distance to objects to detect vehicle presence.
2. **ESP32 and ESP32S Mini**:
   - Processes sensor data and communicates with the gateway and Firebase.
3. **Gateway Device (ESP32S Mini)**:
   - Aggregates data from nodes and sends it to Firebase.

### States:
- **Empty**: Parking spot is available.
- **Full**: Parking spot is occupied.
- **Unknown**: Sensor data is inconclusive.

---

## Software Design

### Mobile Application
- Developed using **Flutter**.
- Integrates `flutter_map` for displaying parking lots on an interactive map.
- Retrieves real-time data from Firebase to display parking statuses.

### Cloud Backend
- Firebase used for real-time data syncing and storage.

### Algorithms
- Distance-based detection using threshold values from ultrasonic sensors.
- State change detection to minimize redundant communication.

---

## Results and Discussion
### Key Outcomes
- Real-time parking space monitoring achieved.
- Mobile application and web dashboard successfully display parking availability.

### Challenges
- Environmental factors affecting sensor accuracy.
- Optimizing communication to minimize latency and power usage.

### Future Improvements
- Enhance sensor accuracy for varying environmental conditions.
- Add support for multiple gateways for large-scale deployment.
- Integrate payment systems for reserving parking spaces.

---

## Sustainable Development Goals (SDGs) Alignment
The **Smart Parking System** contributes to the following SDGs:
1. **SDG 11: Sustainable Cities and Communities**:
   - Reduces traffic congestion and pollution, making urban areas more sustainable.
2. **SDG 13: Climate Action**:
   - Minimizes greenhouse gas emissions by reducing fuel consumption.

---

## Repository Structure
```
comp413-g5-smart-parking-system/
├── README.md           # Overview of the project
├── src/                # Source code for ESP32 and Flutter app
├── docs/               # Documentation and project report (PDF)
├── images/             # Images for dashboard and system architecture
└── demo/               # Video demo (3 mins)
```

---

## How to Set Up

### Hardware Setup
1. Connect HCSR04 sensors to ESP32 devices.
2. Configure the ESP32S Mini as the gateway device.
3. Ensure all devices are connected to the same network.

### Software Setup
1. Clone this repository.
2. Install required libraries for ESP32 microcontrollers using the Arduino IDE.
3. Deploy the Firebase configuration to the ESP32 gateway.
4. Set up the Flutter mobile application:
   ```bash
   flutter pub get
   flutter run
   ```

---

## Live Demo
- **Video Demo**: [Link to 3-minute video demo]
- **Live Dashboard**: [Link to dashboard]

---

## Contributors
- Muhammet Çağrı Akkuş
- Tolgahan Keleş
- Umut Kaya

---

## License
This project is licensed under the MIT License.
