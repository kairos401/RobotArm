import cv2
import numpy as np
import time
from pymycobot.mycobot import MyCobot


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
    cv2.imshow("Mask", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


