import tkinter as tk
import math
import random

# Constants
g = 9.8  # gravity
mass = 1
time_step = 0.03
scale = 5  # scaling factor for display


# Convert force to velocity
def force_to_velocity(force, mass):
    return math.sqrt(2 * force / mass)


# Projectile stats
def projectile_motion(angle_deg, force_input, height_input):
    angle_rad = math.radians(angle_deg)
    v0 = force_to_velocity(force_input, mass)

    # Max height above ground
    max_height = height_input + (v0 ** 2 * math.sin(angle_rad) ** 2) / (2 * g) * random.uniform(0.98, 1.02)

    # Total horizontal distance (solving quadratic y = h + v*sin*t - 0.5*g*t^2)
    # y = 0 -> 0 = height + v*sin*t - 0.5*g*t^2
    a = -0.5 * g
    b = v0 * math.sin(angle_rad)
    c = height_input
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        total_time = 0
        max_distance = 0
    else:
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        total_time = max(t1, t2)
        max_distance = v0 * math.cos(angle_rad) * total_time * random.uniform(0.98, 1.02)

    return v0, angle_rad, max_height, max_distance, total_time


# Launch projectile
def launch():
    canvas.delete("ball")
    angle = float(angle_entry.get())
    force_input = float(force_entry.get())
    height_input = float(height_entry.get())

    v0, angle_rad, max_height, max_distance, total_time = projectile_motion(angle, force_input, height_input)

    info_label.config(
        text=f"Angle: {angle}° | Force: {force_input} | Cannon Height: {height_input} m\nMax Height: {max_height:.2f} m | Distance: {max_distance:.2f} m | Time: {total_time:.2f} s")

    t = 0
    while True:
        x = v0 * math.cos(angle_rad) * t
        y = height_input + v0 * math.sin(angle_rad) * t - 0.5 * g * t ** 2
        if y < 0:
            y = 0
            canvas.create_oval(cannon_x + x * scale - 5, cannon_y - y * scale - 5,
                               cannon_x + x * scale + 5, cannon_y - y * scale + 5,
                               fill="red", tag="ball")
            canvas.update()
            break
        canvas.delete("ball")
        canvas.create_oval(cannon_x + x * scale - 5, cannon_y - y * scale - 5,
                           cannon_x + x * scale + 5, cannon_y - y * scale + 5,
                           fill="red", tag="ball")
        canvas.update()
        t += time_step


# Draw cannon and ground
def draw_cannon():
    canvas.delete("cannon")
    height_input = float(height_entry.get())
    cannon_y_position = cannon_y - height_input * scale
    # Cannon base
    canvas.create_rectangle(cannon_x - 20, cannon_y_position, cannon_x + 20, cannon_y_position + 20, fill="darkgrey",
                            tag="cannon")
    # Cannon barrel
    angle_rad = math.radians(float(angle_entry.get()))
    end_x = cannon_x + 50 * math.cos(angle_rad)
    end_y = cannon_y_position - 50 * math.sin(angle_rad)
    canvas.create_line(cannon_x, cannon_y_position, end_x, end_y, width=15, fill="grey", capstyle=tk.ROUND,
                       tag="cannon")
    # Ground line
    canvas.create_line(0, cannon_y, 800, cannon_y, fill="green", width=4, tag="cannon")


# GUI setup
root = tk.Tk()
root.title("Cannon Projectile Simulator")

canvas = tk.Canvas(root, width=800, height=500, bg="black")
canvas.pack()

cannon_x = 200
cannon_y = 400  # reference ground position

info_label = tk.Label(root, text="", fg="white", bg="black", font=("Arial", 12))
info_label.pack()

# Inputs
tk.Label(root, text="Launch Angle (°):", fg="white", bg="black").pack()
angle_entry = tk.Entry(root)
angle_entry.pack()
angle_entry.insert(0, "45")

tk.Label(root, text="Force:", fg="white", bg="black").pack()
force_entry = tk.Entry(root)
force_entry.pack()
force_entry.insert(0, "200")

tk.Label(root, text="Cannon Height from Ground (m):", fg="white", bg="black").pack()
height_entry = tk.Entry(root)
height_entry.pack()
height_entry.insert(0, "0")

launch_button = tk.Button(root, text="Launch", command=launch)
launch_button.pack()

draw_cannon()


# Update cannon when input changes
def update_cannon(event=None):
    draw_cannon()


angle_entry.bind("<Return>", update_cannon)
height_entry.bind("<Return>", update_cannon)

root.mainloop()
