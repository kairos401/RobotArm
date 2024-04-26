from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)
mc.set_gripper_mode(0)
mc.init_eletric_gripper()

mc.send_angles([0,0,0,0,0,0], 20) #로봇암 영점 시작

mc.set_gripper_state(1,20,1)    #그리퍼 open
time.sleep(0.6)
while mc.is_gripper_moving():
    time.sleep(0.1)

mc.set_gripper_value(20,40)     # 그리퍼 특정각도로 닫기
time.sleep(0.6)
while mc.is_gripper_moving():
    time.sleep(0.1)
    
time.sleep(2)
mc.set_gripper_value(100, 20)   # 그리퍼 열기
time.sleep(0.6)
while mc.is_gripper_moving():
    time.sleep(0.1)