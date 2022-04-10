# Basically Everything

# Bugs
SOLVED?: main.py - set_delta()
- sometimes the value is much too high

# Cleaning


# Bottom Up
0) Test stuff
1) class Enemy(AdvancedHitbox)
    - set up basic things like vision cones, hp/level/dmg/etc
2) class BirdEnemy(Enemy) [or some specific type of enemy]
    - presets, override attack method, etc
3) basic player attacks
    - swing sword
    - basic abilities
4) rooms
5) dungeons
6) menues
7) go back and make everything good
8) saving
9) art


# To Test:
All of the AdvancedHitbox/HitboxPart code
- updating functions
- check_collisions/etc
- is it 'easy' to use?
    - Or will it cause writing Enemy/Player classes to be unessicarly complicated

# Notes
Keys:
- WASD: move player (green)
- Control + Q: quit
- Enter/lmb: change screen from welcome to game
