import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import random, math, time

BG_COLOR = "#000000"
DICE_SIZE = 44


root = tk.Tk()
root.overrideredirect(True)
root.config(bg=BG_COLOR)
root.wm_attributes("-transparentcolor", BG_COLOR)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
root.geometry(f"{screen_w}x{screen_h}+0+0")

canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
canvas.pack(fill="both", expand=True)


dice_x = screen_w // 2
dice_y = screen_h - 70
last_dx = 0
last_dy = 0
dice_angle = 0
vx = 0
vy = 0
final_num = 3
ground = screen_h - 70

current_img = None
start_pos = None
m_animate_id = None
dragging = False
r_animate = False

last_time = time.time()
time_scale = 1.0


def dice_image(num, angle=0):
    size = DICE_SIZE
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [0, 0, size, size],
        radius=10,
        fill=(255, 255, 255, 255),
        outline=(220, 220, 220, 255),
        width=3,
    )

    offset = size / 4 + 2
    spots = {
        1: [(size / 2, size / 2)],
        2: [(offset, offset), (size - offset, size - offset)],
        3: [(offset, offset), (size / 2, size / 2), (size - offset, size - offset)],
        4: [
            (offset, offset),
            (offset, size - offset),
            (size - offset, offset),
            (size - offset, size - offset),
        ],
        5: [
            (offset, offset),
            (offset, size - offset),
            (size - offset, offset),
            (size - offset, size - offset),
            (size / 2, size / 2),
        ],
        6: [
            (offset, offset),
            (offset, size / 2),
            (offset, size - offset),
            (size - offset, offset),
            (size - offset, size / 2),
            (size - offset, size - offset),
        ],
    }

    color = "#ffa500" if num in (1, 4) else "#7f7f7f"
    dot_r = {1: 8.5, 2: 5, 6: 3.6}.get(num, 4.6)

    for x, y in spots[num]:
        x, y = round(x), round(y)
        draw.ellipse((x - dot_r, y - dot_r, x + dot_r, y + dot_r), fill=color)

    rotated = img.rotate(-angle, resample=Image.BICUBIC, expand=True)  # type: ignore
    return ImageTk.PhotoImage(rotated)


def reset(event=None):
    global dice_x, dice_y, last_dx, last_dy, dice_angle, vx, vy, final_num, ground, current_img, dice_item, m_animate_id, dragging, r_animate

    dice_x = screen_w // 2
    dice_y = screen_h - 70
    last_dx = 0
    last_dy = 0
    dice_angle = 0
    vx = 0
    vy = 0
    final_num = 3
    ground = screen_h - 70

    current_img = dice_image(final_num)
    dice_item = canvas.create_image(dice_x, dice_y, image=current_img)
    m_animate_id = None

    dragging = False
    r_animate = False

    canvas.tag_bind(dice_item, "<ButtonPress-1>", start_drag)
    canvas.tag_bind(dice_item, "<B1-Motion>", on_drag)
    canvas.tag_bind(dice_item, "<ButtonRelease-1>", roll_dice_random)
    canvas.tag_bind(dice_item, "<ButtonPress-3>", start_drag)
    canvas.tag_bind(dice_item, "<B3-Motion>", on_drag)
    canvas.tag_bind(dice_item, "<ButtonRelease-3>", roll_dice_6)


def start_drag(event):
    global start_pos, dragging
    start_pos = (event.x, event.y)


def on_drag(event):
    global dice_x, dice_y, last_dx, last_dy, start_pos, dragging, r_animate

    if start_pos:
        dx = event.x - start_pos[0]
        dy = event.y - start_pos[1]
        dist = math.hypot(dx, dy)
        if dist > 10:
            dragging = True
            canvas.move(dice_item, dx, dy)
            start_pos = (event.x, event.y)
            dice_x += dx
            dice_y += dy
            last_dx = dx
            last_dy = dy

            speed = math.hypot(dx, dy)
            if speed > 50 and r_animate == False:
                r_animate = True
                d = random.choice([-25, 25])
                rotate_animation(d)

        else:
            last_dx = 0
            last_dy = 0


def rotate_animation(d):
    global dice_angle, current_img, r_animate

    current_img = dice_image(final_num, dice_angle)
    canvas.itemconfig(dice_item, image=current_img)
    dice_angle += d

    if dragging:
        canvas.after(10, rotate_animation, d)
    else:
        r_animate = False


def roll_dice_random(event=None):
    global vx, vy, final_num, dragging, last_time

    final_num = random.randint(1, 6)
    last_time = time.time()
    d = random.choice([-25, 25])
    vx = last_dx if dragging else 0
    vy = last_dy if dragging else -175

    dragging = False

    stop_main_animation()
    main_animation(final_num, d, dice_angle)


def roll_dice_6(event=None):
    global vx, vy, final_num, dragging, last_time

    final_num = 6
    last_time = time.time()
    d = random.choice([-25, 25])
    vx = last_dx if dragging else 0
    vy = last_dy if dragging else -175

    dragging = False

    stop_main_animation()
    main_animation(final_num, d, dice_angle)


def key_pressed(event):
    global vx, vy, final_num, last_time

    key = event.keysym.lower()

    final_num = random.randint(1, 6)
    last_time = time.time()
    d = random.choice([-25, 25])

    if key == "w":
        vx += 0
        vy += -175
    elif key == "a":
        vx += -200
        vy += -50
    elif key == "s":
        vx += 0
        vy += 175
    elif key == "d":
        vx += 200
        vy += -50
    elif key == "q":
        vx += -100
        vy += -125
    elif key == "e":
        vx += 100
        vy += -125

    elif key in ["1", "2", "3", "4", "5", "6"]:
        final_num = int(key)
    elif key == "r":
        reset()
        return
    elif key == "f":
        final_num = 6
        vx += 0
        vy += -175
    elif key == "t":
        vx = random.randint(-1800, 1800)
        vy = random.randint(-1000, 1000)
    elif key == "g":
        vx += 0
        vy += -175
    else:
        return

    stop_main_animation()
    main_animation(final_num, d, dice_angle)


def main_animation(num, d, angle):
    global dice_x, dice_y, vx, vy, current_img, m_animate_id, last_time, time_scale

    if dragging:
        return

    now = time.time()
    dt = (now - last_time) * 33 * time_scale
    last_time = now

    g = 9.8
    restitution = 0.6
    friction = 0.5

    left_wall = DICE_SIZE / 2
    right_wall = screen_w - left_wall
    ceiling = DICE_SIZE / 2

    dice_x += vx * dt
    vy += g * dt
    dice_y += vy * dt
    angle += d * dt

    if dice_x <= left_wall or dice_x >= right_wall:
        if dice_x == left_wall or dice_x == right_wall:
            friction = 1

        dice_x = max(left_wall, min(right_wall, dice_x))
        vx = -vx * restitution
        vy = vy * friction

    if dice_y <= ceiling:
        dice_y = ceiling
        vx = vx * friction
        vy = -vy * restitution

    if dice_y >= ground:
        vx = vx * friction
        vy = -vy * restitution
        dice_y = ground
        if abs(vy) + abs(vx) * 0.1 < 5:
            dice_y = ground
            canvas.coords(dice_item, dice_x, dice_y)
            current_img = dice_image(num)
            canvas.itemconfig(dice_item, image=current_img)
            return

    canvas.coords(dice_item, dice_x, dice_y)
    current_img = dice_image(random.randint(1, 6), angle)
    canvas.itemconfig(dice_item, image=current_img)
    m_animate_id = root.after(16, lambda: main_animation(num, d, angle))


def stop_main_animation():
    global m_animate_id

    if m_animate_id is not None:
        try:
            root.after_cancel(m_animate_id)
        except tk.TclError:
            pass

        m_animate_id = None


def slow_motion_on(event=None):
    global time_scale
    time_scale = 0.25


def slow_motion_off(event=None):
    global time_scale
    time_scale = 1.0


reset()

root.bind("<Key>", key_pressed)
root.bind("<Control-r>", reset)
root.bind("<ButtonPress-2>", reset)
root.bind("<KeyPress-space>", slow_motion_on)
root.bind("<KeyRelease-space>", slow_motion_off)
root.mainloop()
