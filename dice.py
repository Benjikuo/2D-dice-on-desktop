import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import random, math

BG_COLOR = "#000000"
DICE_SIZE = 44
dice_x = 100
dice_y = 710
current_img = None
start_pos = None
dragging = False
moved = False
final_num = 3
last_dx = 0
last_dy = 0
jump = False


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
    global dice_item, current_img, dice_x, dice_y, final_num, moved
    current_img = dice_image(3)
    dice_x = screen_w / 2
    dice_y = screen_h - 70
    dice_item = canvas.create_image(dice_x, dice_y, image=current_img)
    moved = False

    canvas.tag_bind(dice_item, "<ButtonPress-1>", start_drag)
    canvas.tag_bind(dice_item, "<B1-Motion>", on_drag)
    canvas.tag_bind(dice_item, "<ButtonRelease-1>", roll_dice_random)
    canvas.tag_bind(dice_item, "<ButtonPress-3>", start_drag)
    canvas.tag_bind(dice_item, "<B3-Motion>", on_drag)
    canvas.tag_bind(dice_item, "<ButtonRelease-3>", roll_dice_6)


def start_drag(event):
    global start_pos, dragging, last_dx, last_dy
    start_pos = (event.x, event.y)
    dragging = False


def on_drag(event):
    global start_pos, dragging, dice_x, dice_y, last_dx, last_dy, moved
    moved = True
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


def roll_dice_random(event=None):
    global final_num
    final_num = random.randint(1, 6)
    roll_dice(event)


def roll_dice_6(event=None):
    global final_num
    final_num = 6
    roll_dice(event)


def key_pressed(event):
    global final_num, dragging
    if dragging:
        return

    dragging = False
    key = event.keysym.lower()

    if key in ["1", "2", "3", "4", "5", "6"]:
        final_num = int(key)
    elif key == "r" or key == "space":
        final_num = random.randint(1, 6)
    else:
        return

    roll_dice()


def roll_dice(event=None):
    global dragging, dice_y, final_num, last_dx, last_dy, moved, jump

    if jump:
        return

    vx = last_dx if dragging else 0
    vy = 0 + last_dy if dragging else -25
    ground = 1010 if moved else dice_y
    d = random.choice([-25, 25])

    jump = False if dragging else True
    dragging = False
    animate(dice_y, vx, vy, final_num, d, ground)


def animate(y, vx, vy, num, d, ground, angle=0):
    global current_img, dice_x, dice_y, dragging, jump

    if dragging:
        return

    g = 2.5
    damping = 0.4
    left_wall = 22
    right_wall = screen_w - left_wall
    ceiling = 0

    dice_x += vx
    vy += g
    y += vy
    angle += d

    if dice_x <= left_wall or dice_x >= right_wall:
        vx = -vx * damping
        dice_x = max(left_wall, min(right_wall, dice_x))

    if y <= ceiling:
        y = ceiling
        vy = -vy

    if y >= ground:
        vx = vx * damping
        vy = -vy * damping
        y = ground
        if abs(vy) + abs(vx) * 0.1 < 5:
            jump = False
            dice_y = ground
            canvas.coords(dice_item, dice_x, dice_y)
            current_img = dice_image(num)
            canvas.itemconfig(dice_item, image=current_img)
            return

    canvas.coords(dice_item, dice_x, y)
    current_img = dice_image(random.randint(1, 6), angle)
    canvas.itemconfig(dice_item, image=current_img)
    root.after(20, lambda: animate(y, vx, vy, num, d, ground, angle))


root = tk.Tk()
root.overrideredirect(True)
root.config(bg=BG_COLOR)
root.wm_attributes("-transparentcolor", BG_COLOR)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
root.geometry(f"{screen_w}x{screen_h}+0+0")

canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
canvas.pack(fill="both", expand=True)

reset()

root.bind("<Key>", key_pressed)
root.bind("<Control-r>", reset)
root.bind("<ButtonPress-2>", reset)
root.mainloop()


dice_x = screen_w / 2
dice_y = screen_h - 70
