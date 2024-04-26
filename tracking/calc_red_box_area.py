import cv2
import numpy as np
from pymycobot.mycobot import MyCobot
import time

# 로봇팔 초기화
# mc = MyCobot('/dev/ttyAMA0', 115200)

# 카메라 초기화

mc = MyCobot('/dev/ttyACM0', 115200)
mc.send_coords([-73.40,199.20,337.00,179.55,-7.45,1.78], 20, 0)
time.sleep(0.6)
while mc.is_moving():
    time.sleep(0.1)

cap = cv2.VideoCapture("http://172.30.1.66:8080/?action=stream")

def find_red_object(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2

    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # 가장 큰 윤곽선 찾기
        largest_contour = max(contours, key=cv2.contourArea)
        # 면적 계산
        area = cv2.contourArea(largest_contour)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY, mask, area
    return -1, -1, mask, 0

while True:
    for _ in range(10):  # 버퍼를 지우기 위해 여러 번 grab 호출
        cap.grab()
    ret, frame = cap.retrieve()  # 최신 프레임 가져오기
    x, y, mask, area = find_red_object(frame)
    if x != -1 and y != -1:
        print(f"Area of the red object: {area} pixels")
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
