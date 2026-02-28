import subprocess
from time import sleep
import time
import datetime
import os
import argparse



ALARM_COOLDOWN_SECONDS = 2
last_trigger_time = 0

def play_sound_wav(wav_path="/home/leddy/Downloads/Bong.wav"):
    proc = subprocess.Popen(
        ["aplay", wav_path])
  
   
def people_detector_from_ip(rtsp_url, alarm_action=None):
    print(f"📡 Watching: {rtsp_url}")
    global last_trigger_time
    
    detect_command = (
        f"source /home/leddy/hailo-rpi5-examples/setup_env.sh && "
        f"python /home/leddy/hailo-rpi5-examples/basic_pipelines/bob_eyes_car_person_v1.1.py --input '{rtsp_url}'"
    )
    print('opened bob_eye2')
    
    detect_process = subprocess.Popen(
        detect_command,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        shell=True, executable="/bin/bash",
        text=True, cwd="/home/leddy/hailo-rpi5-examples/basic_pipelines"
    )
     
    try:
        for line in detect_process.stdout:
            #print(f"[BOB output] {line.strip()}")
            if "person" in line.lower():
                now = time.monotonic()
                if now - last_trigger_time >= ALARM_COOLDOWN_SECONDS:
                    last_trigger_time = now
                    print("🚨 PERSON DETECTED")
                    #play_sound_wav()
                else:
                    print("⏳ Skipping duplicate trigger (cooldown active)")
                    
            elif "car" in line.lower():
                now = time.monotonic()
                if now - last_trigger_time >= ALARM_COOLDOWN_SECONDS:
                    last_trigger_time = now
                    print("🚨 CAR DETECTED")
                    #play_sound_wav()
                else:
                    print("⏳ Skipping duplicate trigger (cooldown active)")
                    
    except KeyboardInterrupt:
        print("🛑 Stopping...")
        detect_process.terminate()
        detect_process.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BOB Eyes 3 - Hailo Detection")
    parser.add_argument('--source', required=True, help='Video source (e.g., RTSP URL, file path, etc.)')
    args = parser.parse_args()

    video_source = args.source
    people_detector_from_ip(video_source)

