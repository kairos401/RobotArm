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


def adjust_robot_arm(angles, area):
    global base_angles
    target_area = 1000  # 목표 픽셀 크기
    threshold = 200  # 변화가 일어나지 않는 임계값 범위
    min_area_threshold = 500  # 무시할 최소 픽셀 크기
    changes_val = 10
    new_angles = angles
    if 2000 < min_area_threshold:  # 너무 작은 객체는 무시
        print("빨간색 객체 없음")
        return False 
    
    if 2000 < target_area - threshold: #크기가 작게보이면 가까이 가라 +
        if new_angles[3] > base_angles[3] - 15:  # 최대 이동 범위제한
            print(new_angles)
            new_angles[3] = new_angles[3]-changes_val  # 로봇팔을 앞으로 이동
            print(new_angles)
            print("x값 증가 앞으로 이동")
            time.sleep(0.1)
            return new_angles
        else:
            # print("이동제한 + 15")
            return False
    elif 2000 > target_area + threshold:     # 크기가 크게 보이면 멀어져라 -
        if new_angles[3] < base_angles[3] + 15:  # 최소 이동 범위제한
            print(new_angles)
            new_angles[3] = new_angles[3]+changes_val  # 로봇팔을 뒤로 이동
            print(new_angles)
            print("x값 감소 뒤로 이동")
            time.sleep(100)
            return new_angles
        else:
            # print("이동 제한 - 15")
            return False
    else:
        # print("제자리")
        return False  # 목표 범위 내이므로 변경 없이 유지

# 로봇팔 초기화
mc = MyCobot('/dev/ttyACM0', 115200)
mc.send_angles([0,0,0,0,90,0], 20) #로봇암 영점 시작
time.sleep(0.6)                 #메세지 전달 delay
while mc.is_moving():           # 로봇암이 움직이는 동안 대기
    time.sleep(0.1)             # CPU 사용을 줄이기 위해 작은 대기 시간 추가
base_angles = mc.get_angles()

# 카메라 초기화
cap = cv2.VideoCapture("http://172.30.1.66:8080/?action=stream")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 버퍼 크기를 1로 설정하여 최소화
while True:
    for _ in range(10):  # 버퍼를 지우기 위해 여러 번 grab 호출
        cap.grab()
    ret, frame = cap.retrieve()  # 최신 프레임 가져오기
    x, y, mask, area = find_red_object(frame)
    if x != -1:
        angles = mc.get_angles()
        print(angles)
        if angles:
            new_angles = adjust_robot_arm(angles, area)
            print(f"Area of the red object: {area} pixels")
            if new_angles:
                mc.send_angles(new_angles, 10)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    cv2.imshow("Mask", mask)
cap.release()
cv2.destroyAllWindows()