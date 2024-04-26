from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)

# mc.send_angles([-80,-35,-41,-11,86,13], 20)   #[-80,-35,-41,-11,86,13] / [0,0,0,0,0,0]
for i in range(-154, 154, 5):
    mc.send_angles([i,90,0,0,0,0], 10)
    time.sleep(0.6)         #메세지 전달 delay
    while mc.is_moving():  # 로봇암이 움직이는 동안 대기
        time.sleep(0.1)  # CPU 사용을 줄이기 위해 작은 대기 시간 추가
    coords = mc.get_coords()
    print("X: {:.2f}, Y: {:.2f}, Z: {:.2f}, Rx: {:.2f}, Ry: {:.2f}, Rz: {:.2f}".format(*coords))
