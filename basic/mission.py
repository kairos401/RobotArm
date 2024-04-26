from pymycobot.mycobot import MyCobot
import cv2
import numpy as np
import time

def arm_move_chk():
    time.sleep(0.6)
    while mc.is_moving():
        print("arm is moving")
        time.sleep(0.5)

def gripper_move_chk():
    time.sleep(0.6)
    while mc.is_gripper_moving():
        print("gripper is moving")
        time.sleep(0.5)

def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_ranges = {
        'red': ([0, 120, 70], [10, 255, 255], [170, 120, 70], [180, 255, 255]),
        'yellow': ([25, 70, 120], [35, 255, 255]),
        'blue': ([90, 150, 0], [130, 255, 255]),
        'purple': ([50, 70, 70], [90, 255, 255])
    }
    threshold_area = 1000           # 물체를 인식하는 기준
    detected_color = -1             # Default 값
    for color, ranges in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(ranges[0]), np.array(ranges[1]))
        if len(ranges) == 4:
            mask += cv2.inRange(hsv, np.array(ranges[2]), np.array(ranges[3]))
        # cv2.imshow(f"{color} mask", mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > threshold_area:
                color_to_number = {'red': 0, 'yellow': 1, 'blue': 2, 'green': 3}
                detected_color = color_to_number[color]
    return detected_color

def place_box(i,spd=40,mode=False):
    global pick_pos
    global place_pos
    global stopover_pos
    print(f"물체를 감지!!")
    time.sleep(1)
    print("1. 물건을 집습니다")
    mc.send_coords(pick_pos,spd,mode)
    arm_move_chk()
    time.sleep(1)
    mc.set_gripper_value(20,40)
    gripper_move_chk()
    time.sleep(2)
    print("2. 경유지 1번으로 이동")
    mc.send_coords(stopover_pos[0],spd,mode)
    arm_move_chk()
    print("3. 경유지 2번으로 이동")
    mc.send_coords(stopover_pos[1],spd,mode)
    arm_move_chk()
    print("4. 물건을 놓습니다")
    mc.send_coords(place_pos[i],spd,mode)
    arm_move_chk()
    mc.set_gripper_value(100, 20)
    gripper_move_chk()
    time.sleep(1)
    print("5. 경유지 2번으로 이동")
    mc.send_coords(stopover_pos[1], spd, mode)
    arm_move_chk()
    print("6. 물건 감지 위치로 이동")
    mc.send_coords(setting_pos, spd, mode)
    arm_move_chk()
    print("2초뒤 물체 감지를 시작합니다")
    time.sleep(2)

# 물건 감지 위치
setting_pos = [-73.40,199.20,337.00,179.55,-7.45,1.78]

# 물건 집는 위치
pick_pos = [-63, 268,286,175,-5,91]

# 물건 놓는 위치
place_pos = [
    [-195,-125,310,-180,-4,-143],   #빨
    [-212,-11,300,180,0,165],     #노
    [-200.10,90.50,295.60,176.32,1.13,139.64],      #파
    [-200.10,86.50,289.60,176.32,1.13,139.64]
]
# 경유지 위치
stopover_pos = [
    [-77.80,11.40,477.30,142.54,-84.66,124.20],
    [-153.20, -6.20, 523.80, -90.00, -0.96, 90.79]
]
mc = MyCobot('/dev/ttyACM0', 115200)
#로봇암 영점 시작
mc.set_gripper_mode(0)
time.sleep(0.5)
mc.init_eletric_gripper()
time.sleep(0.5)
mc.send_angles([0,0,0,0,0,0], 20) 
arm_move_chk()
mc.send_coords(stopover_pos[0], 20, 0) 
arm_move_chk()
mc.send_coords(setting_pos, 20, 0) 
arm_move_chk()
print("2초뒤 물체 감지를 시작합니다")
time.sleep(2)

while True:
    cap = cv2.VideoCapture("http://172.30.1.66:8080/?action=stream")
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    for _ in range(10):
        cap.grab()  # Clear buffer
    ret, frame = cap.retrieve()  # Retrieve latest frame
    color = -1
    color = detect_color(frame)
    print(f"색깔은 {color} 입니다.")
    if color != -1:
        place_box(i=color)
        color = -1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    color = -1
    

cap.release()
cv2.destroyAllWindows()