🚗 bob-eyes-hailo8-snapshot-system

Snapshot-based People + Car detection system using Hailo8 + GStreamer.

This repo contains the launcher + detection layer only.

It is designed to run on a Raspberry Pi 5 with a Hailo8 accelerator and an RTSP IP camera.

🔧 What It Does

Detects people and cars

Saves snapshots only when movement is detected

Uses cooldown logic to prevent duplicate captures

Auto-cleans snapshot folders when storage limits are reached

Designed for long-term unattended runtime

🏗 Architecture

This project runs in two layers:

1️⃣ launcher.py

Starts detection pipeline

Feeds RTSP source

Handles cooldown logic

Entry point for system

2️⃣ car_person_detector.py

Runs GStreamer inference

Uses Hailo detection framework

Tracks bounding box movement

Saves snapshots conditionally

Manages folder trimming

📂 Snapshot Storage

Images are saved to:

/home/leddy/snapshots
/home/leddy/snapshots_cars

Folder limits:

Max size: 1000 MB

Auto-trims down to: 700 MB

Oldest files deleted first

🚀 Run
1️⃣ Activate Hailo environment
source /home/leddy/hailo-rpi5-examples/setup_env.sh
2️⃣ Start system
python launcher.py --source "rtsp://YOUR_CAMERA_URL"

Example:

python launcher.py --source "rtsp://192.168.1.50:554/stream"
🎯 Detection Behaviour
👤 Person

Cooldown-based trigger

Saves full-frame snapshot

🚗 Car

Requires ≥ 0.90 confidence

Tracks bounding box position

Saves only when car moves significantly

Prevents stationary duplicate captures

📋 Requirements

You MUST have:

Raspberry Pi 5

Hailo8 installed

HailoRT configured

hailo-rpi5-examples installed

GStreamer working

Python 3.9+

📁 Files

launcher.py

car_person_detector.py

requirements.txt

❗ Not Included

Hailo runtime packages

GStreamer binaries

Model weights

RTSP camera

System service files