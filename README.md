# Santa’s Gift Delivery

**Santa’s Gift Delivery** is a 2D platformer game made with **Pygame Zero**.  
The goal is simple — to help Santa jump across platforms, avoid the Grinch and Snowmen, and collect all the gifts before time runs out.  

---

## Game Description

Santa starts at the bottom of the screen and must reach all the scattered gifts.  
You’ll need to jump across platforms, avoid moving enemies, and stay alive — falling off the screen or touching an enemy ends the game.  
When all gifts are collected, you win!

The game includes:
- A working **menu**, **win**, and **game over** screen  
- **Idle animations** for both Santa and enemies  
- **Background music** and **sound effects** (toggleable)  
- A **platform collision system** without using Pygame physics  
- A **score counter** showing collected gifts  
- Smooth transitions between all game states

---

## Controls

| Action | Key |
|--------|-----|
| Move left / right | Arrow keys |
| Jump | Space |
| Start game | Mouse click on “Start Game” |
| Toggle sound | Mouse click on “Sound” |
| Return to menu | Enter |

---

## Game Elements

- **Hero (Santa):** Has walking, idle, and jumping animations.  
- **Platforms:** Solid surfaces created using `Rect` objects.  
- **Enemies:**  
  - *Grinch* patrols between two points.  
  - *Snowman* floats in circular motion.  
- **Gifts:** Floating collectible items that bounce slightly to look alive.

---

## Assets

All images and sounds used in the project are from free online sources or made by the author.  
They are stored in the `images/` and `sounds/` folders according to Pygame Zero conventions.

---

## How to Run

Make sure you have **pgzero** installed:

pip install pgzero

Then run:

pgzrun main.py
