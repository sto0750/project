# CANNONSHOOTER

## Features

1. Basic Rules
- There are 2 players, each playing one at a time by taking turns.
- The goal is to damage the other player, or make the other player fall down to the bottom
- You can adjust the angle, magnitude of the cannon to hit the desired entity.
    

2. Special features
- Each player gets to shoot at most 3 shots per one turn.
- Each player has a limit to the moving.
- There's wind that changes every turn, affecting the trajectory of the cannonballs.
- There are two kinds of cannons, one shoots one big cannonball, the other shoots 5 small cannonballs.


## Some explanation for the code (Based on Project6_1.py)

The whole code consist of 1. canonical definitions for the code, 2. functions for drawing several informative bars, 3. definitions for the classes, 4. definitions for necessary screens, and finally 5. the main function.

### 1. Canonical Definitions (Not Cannonical)

There is nothing much, defined the width and height of the screen, frame per second, and some colors.

### 2. Functions (For drawing bars)

Since there are quite a lot of informations that the player should consider when playing. Especially, when the player shots for 3 times or move for 300 pixels, the turn is over. Therefore the player has to know that how many shots left or how much distance is left for the movement at certain turn.

All 3 informations are coded in a similar way, by drawing rectangular shape with same height and variable length according to the instances.

Since the parameter 'pct' implies percentage, I have to divide the .moving_restriction by 3, and multiply by 100 and then divide by 3 the .shooting_chance to later put as a parameter.

### 3. Classes

Almost all classes are sampled from the "Shmup" game. 

There are two types of class of "Cannonballs", to represent each kind of cannon. Cannonballs class have timedelay instance, which take a role as a prevention of the cannonballs immediately exploding in front of the shooter(since it is detected as a collision).

The Terrain class is made to represent the terrain(or ground) of the game. I decided to describe it as a group of small rectangular bars stacked up. By using np.random functions, I made bars with random length, stacked randomly beneath the first third of the height.

### 4. Functions

There are three screen-showing functions after the class definitions. I used the show_go_screen from "Shmup".

### 5. The Main Function

The main function consists of following 6 big steps.

1. Looking for the keyboard inputs : I have put every keyboard input actions to this part, from moving the player to the turn switching key(return).

1. all_sprite.update() : this line updates all sprites.

2. Collision Detection

3. Turn over Detection

4. Win/Lose Decision

5. Drawing including drawing function at the beginning.

## Citations
 - background image : "https://www.freepik.com/free-vector/arcade-game-world-pixel-scene_4815143.htm#query=game%20background%20pixel%20terrain&position=1&from_view=search&track=ais">Image by stockgiu
 - cannon(tank) image : "https://www.flaticon.com/free-icons/army" title="army icons">Army icons created by Freepik - Flaticon
 - cannonball image : "https://www.flaticon.com/free-icons/bomb" title="bomb icons">Bomb icons created by Freepik - Flaticon
 - terrain image : https://www.freepik.com/free-vector/computer-game-landscapes-collection_9586315.htm#page=4&query=long%20narrow%20cloud%20platform%20game%20pixel&position=2&from_view=search&track=ais">Image by macrovector
 - Background music : https://freetouse.com/music
