🚀 Bob Eyes Hailo8 Snapshot System

Edge-AI snapshot detection system for Raspberry Pi 5 + Hailo8.
Detects people and cars, saves intelligent snapshots, and automatically manages storage.

Built for long-term unattended RTSP camera monitoring.

📸 What This System Does

✅ Detects people and cars

✅ Saves snapshots only when movement is detected

✅ Uses smart cooldown logic to prevent duplicates

✅ Automatically cleans snapshot folders when storage limits are reached

✅ Designed for RTSP IP cameras

✅ Optimised for low CPU overhead

🧠 Built On

Hailo8 AI Accelerator

GStreamer Detection Pipeline

Hailo RPi Examples Framework

Python 3.9+

🏗 System Architecture

This project runs as a lightweight two-layer system:

1️⃣ Launcher (Top Layer)

Responsible for:

Starting the Hailo detection pipeline

Feeding the RTSP source

Monitoring detection output

Applying global cooldown logic

Acting as the system entry point

python launcher.py --source "rtsp://YOUR_CAMERA_URL"
2️⃣ Detection Pipeline (Core Layer)

Handles:

Running GStreamer inference

Object detection via Hailo framework

Movement tracking logic

Snapshot saving

Folder auto-trimming

This layer:

Tracks car positions using bounding box approximation

Filters detections below confidence threshold

Avoids duplicate captures from stationary objects

🎯 Detection Behaviour
👤 Person Detection

Triggered when a person is detected

Cooldown-based protection against repeated frames

Saves full-frame snapshot

🚗 Car Detection

Requires ≥ 0.90 confidence

Tracks bounding box movement

Saves snapshot only when:

Car moves significantly

OR a new high-confidence car appears

Prevents stationary vehicle spam

📂 Snapshot Storage

Snapshots are saved to:

/home/leddy/snapshots
/home/leddy/snapshots_cars
🧹 Automatic Folder Management

Maximum folder size: 1000 MB

Automatically trims down to: 700 MB

Deletes oldest files first

Designed for long-term 24/7 operation

No manual maintenance required.

🚀 Installation & Running
1️⃣ Activate Hailo Environment
source /home/leddy/hailo-rpi5-examples/setup_env.sh
2️⃣ Run the Launcher
python launcher.py --source "rtsp://YOUR_CAMERA_URL"
Example
python launcher.py --source "rtsp://192.168.1.50:554/stream"
⚙️ Hardware & Software Requirements
Hardware

Raspberry Pi 5

Hailo8 AI Accelerator

RTSP IP Camera

Software

HailoRT installed

hailo-rpi5-examples installed

Python 3.9+

🧩 Smart Design Features

Movement-based triggering

Cooldown duplicate protection

Confidence filtering

Object ID approximation via bounding box tracking

Automatic disk management

Designed for unattended 24/7 edge deployment

Clean two-layer modular structure

🛠 Designed For

Driveway monitoring

Car movement tracking

People detection systems

Lightweight security setups

Edge AI experimentation

Standalone snapshot deployments

📌 Project Structure
bob-eyes-hailo8-snapshot-system/
│
├── launcher.py
├── car_person_detector.py
├── requirements.txt
└── README.md
🔒 Notes

This project relies on the Hailo SDK and Hailo RPi example framework.

Hailo components are system-installed and not included in requirements.txt.

Designed specifically for Hailo8 hardware acceleration.

🧠 Future Expansion

This system can easily be extended with:

GUI monitoring interface

Full object archive mode

Real-time detection dashboard

Systemd auto-start service

Web control panel
