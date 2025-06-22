"""
Author: Jayharish Shivakumar
Project: PID-Based AprilTag Tracking with DJI Tello Drone
Platform: Python, OpenCV, djitellopy, pupil_apriltags
Date: 21st June 2025

Description:
This project enables real-time AprilTag (ID 0) detection and tracking using a DJI Tello drone.
PID controllers are used to adjust yaw (left/right), altitude (up/down), and forward/backward movement based on tag position and size.

MIT Licence
"""

from djitellopy import tello
import cv2
import numpy as np
import time
from pupil_apriltags import Detector

#drone setup
drone = tello.Tello()
drone.connect()
print("Battery: ", drone.get_battery())
drone.streamon()
time.sleep(3)
drone.takeoff()

#AprilTag Detector setup
detector = Detector(families="tag36h11")

#frame setup
FRAME_WIDTH = 960
FRAME_HEIGHT = 720
CENTER_X = FRAME_WIDTH // 2
CENTER_Y = FRAME_HEIGHT // 2

#PID constants
KP_x, KI_x, KD_x = 0.25,0.0002, 0.03
KP_y, KI_y, KD_y = 0.25,0.0002, 0.03
KP_area, KI_area, KD_area = 0.005,0,0.003
x_integral = y_integral = area_integral = 0
area_setpoint = 10000
prev_error_x = prev_error_y = prev_error_area = 0
prev_time = time.time()

#main loop
try:
    while True:
        #get frame and convert it for the detector
        frame = drone.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = detector.detect(gray)
        target_found = False

        for r in results:
            if r.tag_id == 0:
                target_found = True

                #find area of tag
                corners = r.corners
                cx = int(np.mean([pt[0] for pt in corners]))
                cy = int(np.mean([pt[1] for pt in corners]))
                area = cv2.contourArea(np.array(corners, dtype=np.int32))

                #draw tag
                cv2.polylines(frame, [np.int32(corners)], True, (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(frame, "ID = 0", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                #PID
                current_time = time.time()
                dt = current_time - prev_time

                #Horizontal component - yaw
                error_x = CENTER_X - cx
                x_integral += error_x
                x_derivative = (error_x - prev_error_x) / dt
                prev_error_x = error_x

                output_x = output_yaw = int(np.clip(KP_x * error_x + KI_x * x_integral + KD_x * x_derivative, -100, 100))

                #Vertical component - up/down
                error_y = CENTER_Y - cy
                y_integral += error_y
                y_derivative = (error_y - prev_error_y) / dt
                prev_error_y = error_y

                output_y = int(np.clip(KP_y * error_y + KI_y * y_integral + KD_y * y_derivative, -100, 100))

                # Forward/backward based on area
                print("Area: ", area)
                error_area = area_setpoint - area
                area_integral += error_area
                area_derivative = (error_area - prev_error_area)/dt
                prev_error_area = error_area

                output_area = int(np.clip(KP_area * error_area + KI_area * area_integral + KD_area * area_derivative, -100, 100))

                prev_time = current_time

                drone.send_rc_control(0, output_area, output_y, -output_yaw)

        if not(target_found):
            cv2.putText(frame, "Tag ID = 0 not found", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            drone.send_rc_control(0, 0, 0, 0)

        cv2.imshow("AprilTag Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    drone.land()
    drone.reboot()
    drone.end()
    cv2.destroyAllWindows()
