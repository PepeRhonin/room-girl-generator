# room-girl-generator
You can generate random character cards for the game Room Girl (ROOMガール) by Illusion.

It randomizez all the facial parameters and hair. Body parameters, clothing, accessories, etc. are left at default.

The tool is obviously not very convinient to use so far, but at least it works (at least onmy machine :D)

#### Requirements:
Python 3.8+ (I think? I have 3.8.10), pyautogui, numpy, msvcrt
\
that's it I guess

## How to use:
1. Put the path to your game directory in "game-location.txt" (example: C:/Games/RoomGirl).
2. Copy "modified-0.png" from /src to your /UserData/chara/female folder.
3. Run the "shuffle.py" file
4. Run the game, open the character editor (female), go to the "Load" menu and select the card from "modified-0.png" file (like here):

![2022-11-05_23-34-49](https://user-images.githubusercontent.com/26247687/200140265-86b19d39-f0d8-4b35-95f7-55b63d23cfb5.png)

5. Press Q to generate and load a new character (be gentle, give it a second to process and try not to move your mouse too much as it uses input emulation)
6. Press E when you're done and the script will stop
