import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import random, math

BG_COLOR = "#000000"
DICE_SIZE = 44
is_animating = False
current_img = None
start_pos = None
dragging = False
final_num = 3


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
    global dice_item, is_animating, current_img, dice_x, dice_y, final_num
    current_img = dice_image(final_num)
    dice_x = screen_w / 2
    dice_y = screen_h - 70
    dice_item = canvas.create_image(dice_x, dice_y, image=current_img)
    is_animating = False

    canvas.tag_bind(dice_item, "<ButtonPress-1>", start_drag)
    canvas.tag_bind(dice_item, "<B1-Motion>", on_drag)
    canvas.tag_bind(dice_item, "<ButtonRelease-1>", roll_dice_random)
    canvas.tag_bind(dice_item, "<ButtonPress-3>", start_drag)
    canvas.tag_bind(dice_item, "<B3-Motion>", on_drag)
    canvas.tag_bind(dice_item, "<ButtonRelease-3>", roll_dice_6)


def start_drag(event):
    global start_pos, dragging
    start_pos = (event.x, event.y)
    dragging = False


def on_drag(event):
    global start_pos, dragging, dice_x, dice_y
    if start_pos:
        dx = event.x - start_pos[0]
        dy = event.y - start_pos[1]
        dist = math.hypot(dx, dy)
        if dist > 5:
            dragging = True
            canvas.move(dice_item, dx, dy)
            dice_x += dx
            dice_y += dy
            start_pos = (event.x, event.y)


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
    dragging = False
    key = event.keysym.lower()

    if key in ["1", "2", "3", "4", "5", "6"]:
        final_num = int(key)
    elif key == "r":
        final_num = random.randint(1, 6)
    else:
        return

    roll_dice()


def roll_dice(event=None):
    global dragging, dice_y, is_animating, final_num

    if is_animating:
        return
    is_animating = True

    v = 0 if dragging else -25
    ground = 1010
    d = random.choice([-25, 25])

    animate(dice_y, v, final_num, d, ground)


def animate(y, v, num, d, ground, angle=0):
    global is_animating, current_img, dice_x, dice_y
    if not is_animating:
        return

    g = 2.2
    v += g
    y += v
    angle += d

    canvas.coords(dice_item, dice_x, y)

    current_img = dice_image(random.randint(1, 6), angle)
    canvas.itemconfig(dice_item, image=current_img)

    if y < ground:
        root.after(20, lambda: animate(y, v, num, d, ground, angle))
    else:
        dice_y = ground
        canvas.coords(dice_item, dice_x, dice_y)
        current_img = dice_image(num)
        canvas.itemconfig(dice_item, image=current_img)
        is_animating = False


root = tk.Tk()
root.overrideredirect(True)
root.config(bg=BG_COLOR)
root.wm_attributes("-transparentcolor", BG_COLOR)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
root.geometry(f"{screen_w}x{screen_h}+0+0")

dice_x = screen_w / 2
dice_y = screen_h - 70

canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
canvas.pack(fill="both", expand=True)

reset()

root.bind("<Key>", key_pressed)
root.bind("<Control-r>", reset)
root.bind("<ButtonPress-2>", reset)
root.mainloop()
