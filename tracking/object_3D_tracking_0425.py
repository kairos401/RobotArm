# coordination (x,y,z,rx,ry,rz)
# 고정값 : rx = -90, ry = 0, rz = -90 
# 로봇암은 원점(0,0,160) 으로부터 약 360mm 반구에 해당하는 이동범위를 가짐 [X : -380~+380]  [Y : -380~+380] [Z : +160~+523] 

import cv2
import numpy as np
import time
from pymycobot.mycobot import MyCobot

def find_red_object(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask1 + mask2
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

def move_robot_arm(cX, cY, area, frame):
    global cur_coords
    global base_coords
    frame_height, frame_width = frame.shape[:2]
    center_x, center_y = frame_width // 2, frame_height // 2
    
    move_scale = 0.1  # This scale converts pixel deviations to real-world motion
    target_area = 2000  # Target pixel size for the area
    threshold = 500
    backNforth_move_scale = 20  # This scale adjusts how much z should move in response to area difference
    spd = 50
    dx, dy = (cX - center_x), (cY - center_y)  # Inverting dy because y increases downwards
    devi = target_area-area
    
    # Calculate new positions
    if abs(devi)>threshold:
        x_adjust = (target_area - area) / area * backNforth_move_scale
    else: x_adjust = 0
    new_x = cur_coords[0] + x_adjust
    new_y = cur_coords[1] - dx * move_scale
    new_z = cur_coords[2] - dy * move_scale
    

    # Clamp values within the arm's operational boundaries
    print(f"현재좌표 : {cur_coords}")   # 변화전 현재 좌표
    new_x = np.clip(new_x, -150, 150)
    new_y = np.clip(new_y, -150, 150)
    new_z = np.clip(new_z, 300, 450)
    print(f"좌표차이 : {new_x-cur_coords[0]:.2f}, {new_y-cur_coords[1]:.2f}, {new_z-cur_coords[2]:.2f},0,0,0")
    cur_coords = [new_x, new_y, new_z, -90, 0, -90]
    print(f"이동좌표 : {new_x:.2f}, {new_y:.2f}, {new_z:.2f}, -90, 0, -90")
    # Send the new coordinates to the robot arm
    mc.send_coords(cur_coords, speed=spd, mode=0)  # Mode 0 for absolute coordinates
    print(f"이동방향 : 뒤로(+) / 왼쪽(+) / 위로(+)")
    # if abs(new_x)>199 or abs(new_y)>199 or new_z>399 or new_z < 301:
    #     print("한계범위 도달")

mc = MyCobot('/dev/ttyACM0', 115200)
mc.send_angles([0, 0, 0, 0, 90, 0], speed=10)
time.sleep(1)  # Wait for the arm to reach the start position
while mc.is_moving():
    time.sleep(0.1)
base_coords = mc.get_coords()
cur_coords = base_coords.copy()


cap = cv2.VideoCapture("http://172.30.1.66:8080/?action=stream")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer size to minimize lag

while True:
    for _ in range(10):  # 버퍼를 지우기 위해 여러 번 grab 호출
        cap.grab()
    ret, frame = cap.retrieve()  # 최신 프레임 가져오기
    cX, cY, mask, area = find_red_object(frame)
    if area < 600:  # 빨간 물체가 작으면 while문 첫번째로 다시 이동
        continue
    
    if cX != -1 and cY != -1:
        move_robot_arm(cX, cY, area, frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    # cv2.imshow("Mask", mask)

cap.release()
cv2.destroyAllWindows()