from pymycobot.mycobot import MyCobot
import time
def capture_pos():
    
    pass


def main():
    # MyCobot 로봇 초기화
    mc = MyCobot('/dev/ttyACM0', 115200)
    
    # 엔터 입력하면, 로봇팔 힘 빠짐
    input("Caution!! Press Enter to release all servos...")
        
    count = 0
    # 모든 서보의 토크를 해제합니다.
    print("Releasing all servos. Press any key to reactivate them.")
    mc.release_all_servos()
    while count < 100:
        cur_pos = mc.get_coords()
        print(cur_pos)
        count += 1
        time.sleep(0.2)
        

    # 엔터 입력하면, 로봇팔 다시 힘들어옴
    input("Press Enter to reactivate all servos...")

    # 모든 서보의 토크를 재활성화합니다.
    mc.power_on()
    print("All servos have been reactivated.")
    
    coords = mc.get_coords()
    print("Current position : ")
    print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(*coords))


if __name__ == "__main__":
    main()
