# 2D-dice-on-desktop

![License](https://img.shields.io/badge/License-MIT-yellow)
![Language](https://img.shields.io/badge/Language-Python-blue)

A small dice on desktop which can be thrown by clicking or dragging it.  

<p>
  <img src="https://raw.githubusercontent.com/Benjikuo/2D-dice-on-desktop/refs/heads/main/image/wasd_update.gif" width="830">
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
| -------------- | ----------------------- | ----------------- |
| 👆🏻 Drag           | Hold & move                  | Move the dice |
| 🎲 Roll Dice      | Left-click / G               | Roll and land on a random number |
| 🎯 Roll 6         | Right-click / F              | Roll the die and always land on 6 |
| 💨 Random Throw   | T                            | Throw the dice in a random direction |
| 🔢 Set Number     | Number keys 1 ~ 6            | Set the final number; change instantly if already landed |
| ⬆️ Jump           | W                            | Throw the dice upward |
| ⬅️ Move Left      | A                            | Throw the dice left |
| ⬇️ Move Down      | S                            | Throw the dice downward |
| ➡️ Move Right     | D                            | Throw the dice right |
| ↖️ Throw Up-Left  | Q                            | Throw the dice up-left |
| ↗️ Throw Up-Right | E                            | Throw the dice up-right |
| 🔁 Reset          | Middle-click / R or Ctrl + R | Reset position |
| 🐢 Slow Motion    | Hold Space                   | Slow down the dice motion |
| ❌ Exit           | Alt + F4                     | Close the program |

<br>

## 📜 License  
Released under the **MIT License**.  
You are free to use, modify, and share it for learning or personal projects.  
  
**Sometimes even a small dice can roll big ideas. Who knows how this project will turn out!?**
