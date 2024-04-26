from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)
# 원하는 좌표와 각도 설정
target_coords1 = [41.40, -90.80, 430.00, -108.03, 3.72, -84.17]
target_coords2 = [72.20, 171.40, 336.20, -93.81, -2.13, -81.11]
target_coords3 = [183.20, -334.90, 160.20, 91.63, 86.92, 96.64]
# 로봇팔을 해당 좌표로 이동, 여기서 속도를 70으로 설정

mode = False #True
mc.send_coords(target_coords1, 10, mode)
time.sleep(0.6)         #메세지 전달 delay
while mc.is_moving():  # 로봇암이 움직이는 동안 대기
    time.sleep(0.1)  # CPU 사용을 줄이기 위해 작은 대기 시간 추가

mc.send_coords(target_coords2, 10, mode)
time.sleep(2)
coords = mc.get_coords()
print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(*coords))