from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyACM0', 115200)

def get_command():
    print("Enter command (q/a/w/s/e/d/r/f/t/g/y/h/z or 'exit' to quit, or input coords 'x,y,z,rx,ry,rz'):")
    return input().strip()

def is_coords_input(cmd):
    try:
        coords = [float(n) for n in cmd.split(',')]
        if len(coords) == 6:
            return True, coords
        return False, []
    except:
        return False, []

while True:
    cmd = get_command()
    if cmd == 'exit':
        break

    coords_check, coords = is_coords_input(cmd)
    if coords_check:
        mc.send_coords(coords, 20, 0)  # Assuming 0 is the mode for the direct coordinate control
        time.sleep(0.5)  # Delay to allow movement to complete
        continue

    # 각 명령 실행 전 각도를 새로 가져옵니다.
    angles = mc.get_angles()

    if cmd == 'q':
        angles[0] += 1
    elif cmd == 'a':
        angles[0] -= 1
    elif cmd == 'w':
        angles[1] += 1
    elif cmd == 's':
        angles[1] -= 1
    elif cmd == 'e':
        angles[2] += 1
    elif cmd == 'd':
        angles[2] -= 1
    elif cmd == 'r':
        angles[3] += 1
    elif cmd == 'f':
        angles[3] -= 1
    elif cmd == 't':
        angles[4] += 1
    elif cmd == 'g':
        angles[4] -= 1
    elif cmd == 'y':
        angles[5] += 1
    elif cmd == 'h':
        angles[5] -= 1
    elif cmd == 'z':
        coords = mc.get_coords()
        print("Current position: {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(*coords))
    else:
        print("Invalid command")
        continue
    print(angles)
    mc.send_angles(angles, 20)
    time.sleep(0.5)  # 각도 업데이트 후 잠시 대기
