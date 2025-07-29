# 👑 Princess Maze – Escape from the Castle

A Python-based adventure game where a princess must escape a haunted castle while being pursued by a smart dragon. Built using `pygame` and pathfinding algorithms, this project combines game design with AI logic.

---

## 🎮 Gameplay Overview

In **Princess Maze**, the player controls a princess trying to reach the gate and escape the maze, while being chased by a dragon. Each level introduces new challenges:

- 🧊 **Ice Tiles**: Make the player slip back to the starting position.
- 🪨 **Mud Tiles**: Slow down the player by skipping a turn.
- ❤️ **Hearts**: Provide extra lives (the princess starts with 3).
- 🗝️ **Key**: Must be collected to unlock the final gate in each level.
- 🐉 **Dragon**: Actively chases the player using the A* algorithm.

If the dragon catches the princess 3 times – it’s game over.

---

## 🧠 Algorithms Used

- **A\*** pathfinding: The dragon calculates the optimal path to the princess each turn, considering movement cost (ice < floor < mud).
- **BFS (Breadth-First Search)**: Used during level creation to validate that the maze is solvable (e.g., key/gate are reachable).


---

## 🛠️ Requirements

- Python 3.8+
- pygame (install with `pip install pygame`)

---

## 🚀 How to Play

Use the arrow keys to move the princess:

↑ Up, ↓ Down, ← Left, → Right

Your goal is to collect the key and reach the castle gate 🗝️🏰

Avoid the dragon – if it touches you, you lose a heart

You start with 3 hearts ❤️

Touching ice tiles will make you slip back to your starting position

Stepping on mud tiles will delay your turn

You can pick up extra hearts during the level

You can only open the gate after collecting the key

🛠️ How to Run
Make sure you have Python 3.8+ installed

Install dependencies:


pip install pygame

Run the game:

python main.py

💡 Tip: Run from the root folder where main.py is located.




