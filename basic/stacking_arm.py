from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)

#로봇암 영점 시작
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
mc.send_angles([0,0,0,0,0,0], 20) 
time.sleep(0.6)
while mc.is_moving():
    time.sleep(0.1)

# 물건 집는 위치
target_coords_list = [
    [30,300.40,162.60,178.81,-0.85,-86.74],
    [-10.10,304.00,161.00,176.68,-2.49,-87.27],
    [-58.40,300.10,158.80,174.76,-0.57,-87.65],
    [ -112.30,300.50,167.80,175.00,1.55,-87.70]
]

# 물건 놓는 위치
stack_coords_list = [
    [-241.30, 24.80, 252.50,178.75,2.09,-90.17],
    [-242.90, 24.60, 283.20,179.56,2.31,-90.09],
    [-238.90,32.30,295.30,-178.95,1.32,-89.19],
    [-235.30,44.60,325.90,-179.26,-0.83,-91.851]
]

# 경유지 위치
stopover_coords = [-120.10,28.10,417.30,-178.60,29.90,-53.45]
# 쌓는 좌표 공식 [-276, 138, 262 + 20*i, -175.7 , 2.83  , -3.3]
mode = False

def arm_move_chk():
    time.sleep(0.6)
    while mc.is_moving():
        print("arm is moving")
        time.sleep(1)

def gripper_move_chk():
    time.sleep(0.6)
    while mc.is_gripper_moving():
        print("gripper is moving")
        time.sleep(1)


for index, coords in enumerate(target_coords_list):
    mc.send_coords(coords, 20, mode)
    print(f" {index+1}번째 물건 위치로 이동")
    arm_move_chk()
    
    mc.set_gripper_value(20,40)     # 그리퍼 특정각도로 닫기
    gripper_move_chk()
    print(f"{index+1}번째 물건을 집습니다")
    time.sleep(1)
    
    mc.send_coords(stopover_coords, 20, mode)
    arm_move_chk()
    print(f"경유지로 이동합니다.")
    
    mc.send_coords(stack_coords_list[index], 20, mode)
    print(f"{index+1}번째 물건 놓을 위치로 이동")
    arm_move_chk()
    
    mc.set_gripper_value(100, 20)   # 그리퍼 열기
    print(f"{index+1}번째 물건을 놓습니다")
    time.sleep(1)
    
    mc.send_coords(stopover_coords, 20, mode)
    arm_move_chk()
    print(f"경유지로 이동합니다.")
    

