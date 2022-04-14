# Basically Everything

# Bugs
- Fixed?: Enemy.check_vision()
    - False negative caused by the fact that angles can be negative
    - Ex: -10 degress = 350 degrees


# Cleaning


# Bottom Up
1) class Enemy(AdvancedHitbox)
    - Fix vision cones
2) basic combat
    - swing sword
    - basic abilities?
    - enemy can attack
3) class BirdEnemy(Enemy) [or some specific type of enemy]
    - presets, override attack method, etc
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
