import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo
import datetime
import time



from hailo_apps_infra.hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from hailo_apps_infra.detection_pipeline import GStreamerDetectionApp


class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.last_trigger_time = 0
        self.cooldown_seconds = 0.5
        self.car_positions = {}

    def can_trigger(self):
        now = time.time()
        if now - self.last_trigger_time >= self.cooldown_seconds:
            self.last_trigger_time = now
            return True
        return False
    
    def update_car(self, car_id, cx, cy, confidence, movement_threshold=30, trigger_on_new=True, min_confidence=0.9):
        now = time.time()
        last = self.car_positions.get(car_id)
        if last:
            old_cx, old_cy, last_time = last
            dx = abs(cx - old_cx)
            dy = abs(cy - old_cy)
            if (dx > movement_threshold or dy > movement_threshold) and (now - last_time >= self.cooldown_seconds):
                self.car_positions[car_id] = (cx, cy, now)
                return True
        else:
            self.car_positions[car_id] = (cx, cy, now)
            if trigger_on_new and confidence >= min_confidence:
                print(f"🚗 New high-confidence car: ID={car_id} ({confidence:.2f})")
                return True
        return False
    

    
    def cleanup_old_cars(self, expiry_seconds=1000):
        now = time.time()
        to_delete = [car_id for car_id, (_, _, last_time) in self.car_positions.items()
                     if now - last_time > expiry_seconds]
        for car_id in to_delete:
            del self.car_positions[car_id]



def get_folder_size_mb(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # in MB

def trim_folder_to_target(path, max_mb=1500, target_mb=1000):
    current_size = get_folder_size_mb(path)
    if current_size <= max_mb:
        return

    print(f"⚠️ Folder size {current_size:.2f} MB > {max_mb} MB. Trimming to {target_mb} MB...")

    files = [os.path.join(path, f) for f in os.listdir(path)]
    files = [f for f in files if os.path.isfile(f)]
    files.sort(key=os.path.getctime)

    for file in files:
        try:
            os.remove(file)
            print(f"🗑️ Deleted: {file}")
        except Exception as e:
            print(f"⚠️ Could not delete {file}: {e}")
        if get_folder_size_mb(path) <= target_mb:
            break

def save_frame_directly(frame, prefix):
    folder = f"/home/leddy/snapshots{'_cars' if prefix == 'car' else ''}"
    os.makedirs(folder, exist_ok=True)

    # Trim folder if needed
    trim_folder_to_target(folder, max_mb=1000, target_mb=700)

    # Save the frame
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/{prefix}_{timestamp}.jpg"
    success = cv2.imwrite(filename, frame)
    if not success:
        print("❌ Failed to save snapshot!")


def app_callback(pad, info, user_data):
    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK

    user_data.increment()
    user_data.cleanup_old_cars()
    
    format, width, height = get_caps_from_pad(pad)
    
    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)
        
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    unique_detections = set()
    for detection in detections:
        label = detection.get_label()
        confidence = detection.get_confidence()
        unique_detections.add((label, confidence))

        person_detected = any(label.lower() == "person" for label, _ in unique_detections)
        #rint(frame)
        # Only pull and use the frame if enabled
        label = detection.get_label()
            
        if person_detected and user_data.can_trigger():
            
            frame = get_numpy_from_buffer(buffer, format, width, height)
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                print("🚨 Person detected - saving snapshot")
                save_frame_directly(frame, "person")
                
            else:
                print("Warning: No frame available to save on person detection.")

        if label.lower() == "car":
            if confidence < 0.9:
                continue  # Igno
            bbox = detection.get_bbox()
            x1 = int(bbox.xmin() * width)
            y1 = int(bbox.ymin() * height)
            x2 = int(bbox.xmax() * width)
            y2 = int(bbox.ymax() * height)

            #print(f"📦 Raw car bbox: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

            #x1, y1, x2, y2 = bbox.xmin(), bbox.ymin(), bbox.xmax(), bbox.ymax()
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            #car_id = f"{round(cx)}_{round(cy)}"
            #car_id = f"{round(cx, -1)}_{round(cy, -1)}"  # e.g., 270 instead of 273
            #car_id = f"{round(cx, -1)}_{round(cy, -1)}_{round(x2 - x1)}x{round(y2 - y1)}"
            car_id = f"{round(cx, -2)}_{round(cy, -2)}_{round((x2 - x1)/10)}x{round((y2 - y1)/10)}"

            #print(f"🧭 Car detected: ID={car_id}, Pos=({cx},{cy})")
            if user_data.update_car(car_id, cx, cy, confidence):
            #if user_data.update_car(car_id, cx, cy):
                frame = get_numpy_from_buffer(buffer, format, width, height)
                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    print("🚗 Car moved - saving snapshot")
                    save_frame_directly(frame, "car")


        user_data.set_frame(frame)

    # Print detected objects
    #print("Detected Objects:")
    #for label, confidence in unique_detections:
    #    print(f"Detection: {label} {confidence:.2f}")

    return Gst.PadProbeReturn.OK


if __name__ == "__main__":

    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()


