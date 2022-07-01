# Basically Everything

# Bugs


# Cleaning
- REMOVE GET + SET
- LOAD MAGIC NUMBERS FROM JSON FILE
- REPLACE HITBOX/ADVANCED HITBOX COLLISIONS WITH PYGAME MASKS
- USE TOGGLE CLASS
- USE JSON OR SOMETHING ELSE FOR SAVING/LOADING RATHER THAN .TXT
- IMPROVE VARIABLE NAMES
	- "is_sliding" -> "sliding"
	- "can_fly" -> "flying"
- RUN FORMATER
- USE PYLINT
- "if not self.is_sliding and is_sliding"
	- ?????????????????????
	- ???????????????????????
- FIX BRANCHES
	- DELETE OLD ONES
	- MERGE ANY?
	- SWITCH TO A DIFFERENT BRANCH SET UP
		- "Main" would be only merges

# Bottom Up
1) Make player movement
2) Make things for player to interact with
	- Walls
	- platforms
	- things that insta kill you and send you back to the start
3) make a section of a map
	- like, one screen size
	- each screen size is like 1/40 of the map (number subject to change)
	- test to see if the section is doable
4) Make a full map
	- winning
	- starting thingy
5) Keep a timer of how long it takes
6) menus
7) go back and make everything good
8) saving
	- not saving checkpoints like in Neocrosser, that defeats the purpose.
	- It is just saving and loading the map so we don't have giant lists in the main file
9) art
10) sound effects
11) multiplayer?
	- Racing others?


# To Test:


# Notes
Keys:
- WASD: move player (green)
- Control + Q: quit
- Enter/lmb: change screen from welcome to game

# Unique thingy majigy ideas
- Unique movement
	- sliding/double jump
	- movement changes per map, but not completely
