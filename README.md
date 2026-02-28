# bob-eyes-hailo8-snapshot-system
Standalone Hailo-based object detection system, detects car and people, saves and flushes folders. 
Detects people and cars

Saves snapshots only when movement is detected

Uses cooldown logic to prevent duplicate images

Auto-cleans snapshot folders when storage limit is reached

Designed for RTSP IP cameras

Built on:

Hailo AI accelerator

GStreamer detection pipeline

Hailo RPi examples framework

🏗 Architecture

This system consists of two layers:

1️⃣ Launcher (Top Layer)

Starts the Hailo detection pipeline

Monitors detection output

Handles trigger cooldown logic

2️⃣ Detection Pipeline (Core Layer)

Runs GStreamer inference pipeline

Uses Hailo detection framework

Tracks object movement

Saves images only when:

Person detected (with cooldown)

Car moves position significantly

Automatically trims snapshot folders when exceeding size limit

📂 Snapshot Storage

Images are saved to:

/home/leddy/snapshots
/home/leddy/snapshots_cars

Folder limits:

Max size: 1000 MB

Auto-trims down to: 700 MB

🚀 How To Run
1️⃣ Activate Hailo environment
source /home/leddy/hailo-rpi5-examples/setup_env.sh
2️⃣ Run launcher
python launcher.py --source "rtsp://YOUR_CAMERA_URL"

Example:

python launcher.py --source "rtsp://192.168.1.50:554/stream"
⚙️ Detection Behaviour
👤 Person Detection

Cooldown-based trigger

Saves full-frame snapshot

🚗 Car Detection

Requires 0.9+ confidence

Tracks bounding box position

Saves snapshot only if car moves significantly

Prevents duplicate stationary captures

🧠 Smart Features

Movement-based triggering

Confidence filtering

Object ID approximation

Automatic cleanup of old images

Low CPU overhead

Optimised for long-term unattended running

📋 Requirements

Raspberry Pi 5

Hailo AI accelerator

HailoRT installed

hailo-rpi5-examples installed

Python 3.9+

🛠 Designed For

Driveway monitoring

Car detection

People detection

Lightweight edge AI deployments

Standalone snapshot systems
