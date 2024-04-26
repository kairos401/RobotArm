import cv2
import numpy as np
import time
from pymycobot.mycobot import MyCobot

def find_red_object(image):
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Red color mask
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask1 + mask2

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY, mask, area
    return -1, -1, mask, 0

def adjust_robot_arm(area):
    global base_angles
    global prev_angles
    target_area = 3000  # Target pixel size
    threshold = 400  # Threshold for no action
    min_area_threshold = 700  # Minimum area to ignore
    max_deviation = 20  # Max deviation in degrees
    deviation_scale = 0.005  # Scaling factor for motion based on deviation

    if area < min_area_threshold:
        print("빨간 물체가 없습니다")
        return False
    if target_area-threshold < area < target_area + threshold:
        print("타겟 범위 안에 있습니다")
        return False
    deviation = (area-target_area)  # Calculate deviation from target area
    angle_adjustment = np.clip(deviation * deviation_scale, -max_deviation, max_deviation)

    new_angle = prev_angles[3] + angle_adjustment
    # Ensure the new angle is within the allowable range
    if base_angles[3] - max_deviation <= new_angle <= base_angles[3] + max_deviation:
        prev_angles[3] = new_angle
        print(f"다음 각도{angle_adjustment}를  이 각도{new_angle}로 맞춥니다.")
        return prev_angles
    else:
        print("최대 이동값을 벗어났습니다.")
        return False

# Initialization
mc = MyCobot('/dev/ttyACM0', 115200)
mc.send_angles([0,0,0,0,90,0], 20)
time.sleep(0.6)
while mc.is_moving():
    time.sleep(0.1)

base_angles = mc.get_angles()
prev_angles = mc.get_angles().copy()

# Camera setup
cap = cv2.VideoCapture("http://172.30.1.66:8080/?action=stream")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer size to reduce lag

while True:
    for _ in range(10):
        cap.grab()  # Clear buffer
    ret, frame = cap.retrieve()  # Retrieve latest frame
    x, y, mask, area = find_red_object(frame)
    if x != -1:
        new_angles = adjust_robot_arm(area)
        if new_angles:
            mc.send_angles(new_angles, 10)
        print(f"Area of the red object: {area} pixels")
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    # cv2.imshow("Mask", mask)

cap.release()
cv2.destroyAllWindows()