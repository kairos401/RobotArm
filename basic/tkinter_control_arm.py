import tkinter as tk
from tkinter import ttk
from pymycobot.mycobot import MyCobot

mc = MyCobot('/dev/ttyACM0', 115200)
# 그리퍼를 사용하기 전에 모드 설정과 초기화
mc.set_gripper_mode(0)  # 0 for general mode
mc.init_eletric_gripper()

root = tk.Tk()
root.title("MyCobot Angle and Coordinate Controller")
root.geometry("600x800")  # Set the window size to 600x800

def update_angle(value, slider, index):
    angle = slider.get()
    angles = mc.get_angles()
    angles[index] = angle
    mc.send_angles(angles, 20)
    angle_labels[index].config(text=f"{angle:.2f}°")
    print(f"Set joint {index+1} to {angle:.2f} degrees")

def update_status():
    angles = mc.get_angles()
    coords = mc.get_coords()
    live_angle_label.config(text=f"Live Angles: {angles}")
    live_coord_label.config(text=f"Live Coordinates: {coords}")
    root.after(1000, update_status)  # Schedule next update in 1 second

def set_values(entries, command):
    try:
        values = [float(v) for v in entries.get().split(",")]
        if len(values) == 6:
            command(values, 20)
            print(f"Set values to: {values}")
            if command == mc.send_angles:
                for i, angle in enumerate(values):
                    sliders[i].set(angle)
                    angle_labels[i].config(text=f"{angle:.2f}°")
            else:
                set_coords_label.config(text=f"Set Coordinates: {values}")
        else:
            print("Please enter exactly 6 values.")
    except ValueError:
        print("Please ensure all inputs are valid numbers.")

def set_gripper(value):
    int_value = int(value)  # Convert float to integer
    mc.set_gripper_value(int_value, 20)
    print(f"Set gripper to {int_value}")

sliders = []
angle_labels = []
for i in range(6):
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=i, column=0, sticky=(tk.W, tk.E))

    label = ttk.Label(frame, text=f"Joint {i+1}:")
    label.pack(side=tk.LEFT)

    slider = ttk.Scale(frame, from_=-180, to=180, orient=tk.HORIZONTAL)
    slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    slider.set(mc.get_angles()[i])
    slider.bind("<B1-Motion>", lambda event, s=slider, idx=i: update_angle(event, s, idx))
    sliders.append(slider)

    angle_label = ttk.Label(frame, text=f"{slider.get():.2f}°")
    angle_label.pack(side=tk.LEFT)
    angle_labels.append(angle_label)

# Gripper control
gripper_frame = ttk.Frame(root, padding=10)
gripper_frame.grid(row=6, column=0, sticky=(tk.W, tk.E))
gripper_label = ttk.Label(gripper_frame, text="Gripper:")
gripper_label.pack(side=tk.LEFT)
gripper_scale = ttk.Scale(gripper_frame, from_=0, to=100, orient=tk.HORIZONTAL)
gripper_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
gripper_button = ttk.Button(gripper_frame, text="Set Gripper", command=lambda: set_gripper(gripper_scale.get()))
gripper_button.pack(side=tk.LEFT)

# Entry and Button for Angles
angle_entry = ttk.Entry(root, width=40)
angle_entry.grid(row=7, column=0, pady=10, padx=10)
set_angles_button = ttk.Button(root, text="Set Angles", command=lambda: set_values(angle_entry, mc.send_angles))
set_angles_button.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(10, 20))

# Entry and Button for Coordinates
coord_entry = ttk.Entry(root, width=40)
coord_entry.grid(row=9, column=0, pady=10, padx=10)
set_coords_button = ttk.Button(root, text="Set Coordinates", command=lambda: set_values(coord_entry, mc.send_coords))
set_coords_button.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=(10, 20))

# Set Coordinates label
set_coords_label = ttk.Label(root, text="Set Coordinates: None")
set_coords_label.grid(row=11, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

# Real-time status labels
live_angle_label = ttk.Label(root, text="Live Angles: None", font=('Helvetica', 10))
live_angle_label.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
live_coord_label = ttk.Label(root, text="Live Coordinates: None", font=('Helvetica', 10))
live_coord_label.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

# Start updating angles and coordinates
root.after(1000, update_status)  # Initial delay of 1 second to start the updates

root.mainloop()