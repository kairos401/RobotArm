from pymycobot.mycobot import MyCobot
import time

class twist:
    def __init__(self,lx,ly,lz,ax,ay,az,speed):
        self.lx=lx
        self.ly=ly
        self.lz=lz
        self.ax=ax
        self.ay=ay
        self.az=az
        self.speed=speed

#mc=MyCobot('COM4',115200)
mc=MyCobot('COM5',115200)

mc.send_angles([0,0,0,0,0,0],30)
time.sleep(3)

#t=twist(-300,-50,280,-170,0,70,20)
t=twist(-220,-50,280,-170,0,70,20)
mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)
time.sleep(3)


def main_menu():
    print("-------------------------------------------------")
    print(" LIST MENU")
    print("-------------------------------------------------")
    print(" 0. mc.send_angles([0,0,0,0,0,0],30)")
    print(" 1. linear  x +10")
    print(" 2. linear  x -10")
    print(" 3. linear  y +10")
    print(" 4. linear  y -10")
    print(" 5. linear  z +10")
    print(" 6. linear  z -10")
    print(" a. angular x +10")
    print(" b. angular x -10")
    print(" c. angular y +10")
    print(" d. angular y -10")
    print(" e. angular z +10")
    print(" f. angular z -10")
    print(" G. -300, -50, 280, -170, 0, 70")
    print(" Z. Tracking")
    print("-------------------------------------------------")
    print(" q.  QUIT");
    print("-------------------------------------------------")
    print()
    #print("SELECT THE COMMAND NUMBER : ")
    key = input("SELECT THE COMMAND NUMBER : ")
    return key

def main():
    while True:
        print(t.lx,t.ly,t.lz,t.ax,t.ay,t.az)
        print(t.speed)

        #user_input = input("Press 'a' to show the state: ")
        user_input = main_menu()
        if user_input == '0':
            mc.send_angles([0,0,0,0,0,0],30)
            mc.power_on()

        elif user_input == '1':
            t.lx+=10
            if t.lx>-50:
                t.lx=-50
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '2':
            t.lx-=10
            if t.lx<-320:
                t.lx=-320
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '3':
            t.ly+=10
            if t.ly>140:
                t.ly=140
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '4':
            t.ly-=10
            if t.ly<-140:
                t.ly=-140
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '5':
            t.lz+=10
            if t.lz>290:
                t.lz=290
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '6':
            t.lz-=10
            if t.lz<50:
                t.lz=50
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '7':
            t.speed+=1
            if t.speed>40:
                t.speed=40
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == '8':
            t.speed-=1
            if t.speed<0:
                t.speed=0
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        ###############################################################
        elif user_input == 'a':
            t.ax+=10
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'b':
            t.ax-=10
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'c':
            t.ay+=10
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'd':
            t.ay-=10
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'e':
            t.az+=10
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'f':
            t.az-=10
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)


        ###############################################################
        elif user_input == 'A':
            #mc.send_coords([(-50),(-50),489,(-92),3,(-139)],20,0)
            t.lx,t.ly,t.lz,t.ax,t.ay,t.az = (-50),(-50),489,(-92),3,(-139)
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'B':
            t.lx,t.ly,t.lz,t.ax,t.ay,t.az = (-50),(-30),400,(-92),3,(-139)
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'C':
            mc.send_coords([(550),(-87),320,(-92),3,(-139)],20,0)

        elif user_input == 'D':
            mc.send_coords([(550),(-87),320,(-92),3,(-139)],20,0)

        elif user_input == 'E':
            t.lx,t.ly,t.lz,t.ax,t.ay,t.az = -330, -50, 279, -92, 3, 71
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'F':
            t.lx,t.ly,t.lz,t.ax,t.ay,t.az = -330, -50, 279, -172, 3, 71
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'G':
            t.lx,t.ly,t.lz,t.ax,t.ay,t.az = -300, -50, 280, -170, 0, 70
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        elif user_input == 'H':
            t.lx,t.ly,t.lz,t.ax,t.ay,t.az = -220, -50, 280, -170, 0, 70
            mc.send_coords([t.lx,t.ly,t.lz,t.ax,t.ay,t.az],t.speed,0)

        ###############################################################
        elif user_input == 'q':
            mc.send_angles([0,0,0,0,0,0],30)
            print("You pressed 'q'. Exiting the loop.")
            time.sleep(3)
            break  # 'a'를 입력받으면 반복문을 종료합니다.

if __name__ == "__main__":
    main()

'''
-50 -50 279 -172 3 71     안쪽으로 최대
-320 -50 279 -172 3 71    바깥쪽으뢰 최대

-300 140 280 -170 0 70    왼쪽으로 최대
-300 -140 280 -170 0 70   오른쪽으로 최대
'''