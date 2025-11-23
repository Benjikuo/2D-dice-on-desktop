# 2D-dice-on-desktop
A small dice on desktop which can be thrown by clicking or dragging it.  

<p>
  <img src="https://raw.githubusercontent.com/Benjikuo/2D-dice-on-desktop/refs/heads/main/image/drag_animation.gif" width="800">
</p>

<br>

## 🛠️ Why I Built This
- Sometimes, it's hard to make a decision. So I need a dice to help me.
- It would be cool to have a little dice bouncing around the desktop.
- Watching the dice bouncing around is very relaxing.

<br>

## 🧩 Features
- 🎲 **Click to Roll** – Generates a random dice number with smooth bounce animation  
- 👆🏻 **Drag to Throw** – Simulates motion and gravity when release the dice after dragging 
- 🎯 **Land on Six** – It will always lands on six when user using right click
- 📄 **Single-file Project** – Simple, lightweight, and easy to modify  

<br>

## 📂 Project Structure
```
Desktop dice/
├── image/         # Demonstration gif
├── dice.py        # Main executable script
├── LICENSE        # MIT license
└── README.md      # Project documentation
```

<br>

## ⚙️ Requirements
Install dependencies before running:
```bash
pip install pillow
```

<br>

## ▶️ How to Run
1. Clone & run:
```bash
git clone https://github.com/Benjikuo/2D-dice-on-desktop.git
python dice.py
```
2. Click or drag the dice to interact and have fun!  

<br>

## 💻 Keyboard and Mouse Controls
| Action         | Mouse / Key             | Description       |
|----------------| ------------------------|-------------------|
| 🎲 Roll Dice   | Left-click / R or space | Roll randomly     |
| 🎯 Roll 6      | Right-click / 6         | Always land on 6  |
| 🔢 Roll number | 1 ~ 6                   | Land on 1 ~ 6     |
| 👆🏻 Drag        | Hold & move             | Move the dice     |
| 🔁 Reset       | Middle-click / Ctrl + R | Reset position    |
| ❌ Exit        | Alt + F4                | Close the program |

<br>

## 📜 License  
This project is released under the **MIT License**.  
You are free to use, modify, and share it for learning or personal projects.  
  
**Sometimes even a small dice can roll big ideas. Who knows how this project will turn out!?**
