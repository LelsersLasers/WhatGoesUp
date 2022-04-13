# Basically Everything

# Bugs
angle = math.atan(self.get_y()/self.get_x()) * 180/math.pi
- zero division error

# Cleaning


# Bottom Up
1) class Enemy(AdvancedHitbox)
    - set up basic things like vision cones, hp/level/dmg/etc
2) class BirdEnemy(Enemy) [or some specific type of enemy]
    - presets, override attack method, etc
3) basic player attacks
    - swing sword
    - basic abilities
4) walls/obstacles/vision/scene setting
5) rooms
6) dungeons
7) menues
8) go back and make everything good
9) saving
10) art


# To Test:


# Notes
Keys:
- WASD: move player (green)
- Control + Q: quit
- Enter/lmb: change screen from welcome to game
