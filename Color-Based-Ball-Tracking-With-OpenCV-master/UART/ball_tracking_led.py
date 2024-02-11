import numpy as np
import cv2
import argparse
import time
import serial

vs = cv2.VideoCapture(1)

time.sleep(2.0)

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 480)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

cv2.waitKey(1)

# Configure serial communication with Arduino
arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
time.sleep(0.1)  # Wait for serial to open

while True:
    ret, frame = vs.read()
    if not ret:
        break
    
    blurred = cv2.GaussianBlur(frame, (17, 17), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max]) 
    mask = cv2.inRange(hsv, lower, upper)

    # Increase iterations for better noise reduction
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    # Apply Gaussian blur for additional noise reduction
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        if M['m00'] != 0:
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # Draw a rectangle around the central region
                frame_width = frame.shape[1]
                central_region = frame_width // 4  # Adjust the central region size
                region_start = central_region
                region_end = 3 * central_region
                cv2.rectangle(frame, (region_start, 0), (region_end, frame.shape[0]), (255, 0, 0), 2)

                # Determine position with a narrower central region
                if center[0] < central_region:
                    position_text = "Left"
                    arduino_command = "led2"
                elif center[0] > 3 * central_region:
                    position_text = "Right"
                    arduino_command = "led1"
                else:
                    position_text = "Center"
                    arduino_command = "led_both"

                # Send the command to Arduino
                arduino.write(arduino_command.encode())

                cv2.putText(frame, f"Position: {position_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()
vs.release()
