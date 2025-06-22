# 🚁 AprilTag PID Tracking with DJI Tello

> **Author:** Jayharish Shivakumar  
> **Date:** 21st June 2025  
> **License:** MIT  
> **Platform:** Python, OpenCV, djitellopy, pupil_apriltags  
> **Drone:** DJI Tello  
> **Tag Family:** tag36h11

---

## 📌 Project Description

This project uses a **DJI Tello drone** to detect and track an **AprilTag** (ID = 0) in real-time using a **PID controller**. The drone automatically adjusts its:
- **Yaw** (rotation left/right),
- **Altitude** (up/down),
- **Forward/backward** motion

based on the **position and size of the tag** in the video feed.

---

## 📂 Project Structure

```plaintext
apriltag_tracking_PID.py         # Main code for AprilTag detection and tracking
README.md                        # This file
requirements.txt                 # List of dependencies
```

---

## 🧠 How It Works

1. The Tello drone streams frames via `djitellopy`.
2. Frames are resized and converted to grayscale.
3. AprilTags are detected using `pupil_apriltags`.
4. If tag with ID 0 is found:
   - **Center coordinates and area** are calculated.
   - PID controllers compute corrections for:
     - Yaw (horizontal)
     - Altitude (vertical)
     - Distance (forward/backward)
   - Drone adjusts itself in real-time using `send_rc_control`.
5. If no tag is detected, the drone hovers and shows a warning message on the frame.

---

## ⚙️ PID Control Parameters

These values control how aggressively the drone responds to errors.

```python
# Yaw control (X-axis)
KP_x, KI_x, KD_x = 0.25, 0.0002, 0.03

# Altitude control (Y-axis)
KP_y, KI_y, KD_y = 0.25, 0.0002, 0.03

# Forward/backward based on tag area
KP_area, KI_area, KD_area = 0.005, 0, 0
area_setpoint = 10000
```

Tweak these to better fit your room size, lighting, or tag size.

---

## ▶️ Run the Code

### 🧰 Requirements

- Python 3.7+
- `djitellopy`
- `opencv-python`
- `pupil-apriltags`
- `numpy`

### 🔧 Installation

```bash
pip install -r requirements.txt
```

> If you're using Python 3.12+, note that `pupil_apriltags` may require building from source or using a wheel compatible with your version.

### 🚀 Start Tracking

```bash
python apriltag_tracking_PID.py
```

> Press `q` to stop and land the drone safely.

---

## ⚠️ Safety Notes

- Use in a spacious indoor environment.
- Ensure no people or fragile objects are nearby.
- Do not run near mirrors or bright reflective surfaces.
- Always keep a finger near the emergency land (`drone.land()`) key combo.

---

## ✅ Tested With

- DJI Tello Drone (standard firmware)
- MacBook M1 (Python 3.12.3)
- AprilTag printed at 15x15 cm
- tag36h11 family

---

## 📜 License

This project is licensed under the **MIT License**.  
See [`LICENSE`](LICENSE) file for more details.

---

## 🙌 Credits

Inspired by the vision and control systems of autonomous robotics.

---

### Connect with me:

[LinkedIn](https://www.linkedin.com/in/jayharish-shivakumar-18591b275?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BJ8gsKPwrTfK399uKGHno3w%3D%3D)


