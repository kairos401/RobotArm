from pymycobot.mycobot import MyCobot
import time
mc = MyCobot('/dev/ttyACM0', 115200)
time.sleep(0.6)
while mc.is_moving():
    time.sleep(0.1)
    
coords = mc.get_coords()
print("coords : {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(*coords))

angles = mc.get_angles()
print("angles : {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(*angles))
