from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)
# 원하는 좌표와 각도 설정
target_angle1 = [0,0,0,0,90,0]
target_angle2 = [0,0,0,0,0,0]
target_angle3 = [10,10,-10,-10,20,20]
# 로봇팔을 해당 좌표로 이동, 여기서 속도를 70으로 설정

mc.send_angles(target_angle1, 10)
time.sleep(0.6)         #메세지 전달 delay
while mc.is_moving():  # 로봇암이 움직이는 동안 대기
    time.sleep(0.1)  # CPU 사용을 줄이기 위해 작은 대기 시간 추가
time.sleep(2)

coords = mc.get_coords()
print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(*coords))
