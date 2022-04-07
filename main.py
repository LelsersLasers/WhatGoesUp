from __future__ import annotations
import pygame
# from pygame.locals import *
from classes import Vector, Hitbox

win = None

def createWindow() -> pygame.Surface:
	pygame.init()
	# win = pygame.display.set_mode((600, 600), FULLSCREEN)
	win = pygame.display.set_mode((800, 800))
	x, y = win.get_size()
	size = (x, y * .8)
	pygame.display.set_caption("Some game that is subterranean: v0.00")
	return win



def main():
	win = createWindow()
	hb1 = Hitbox(Vector(100, 100), 100, 100)
	hb2 = Hitbox(Vector(400, 400), 100, 100)


	while True:
		keys_down = pygame.key.get_pressed()
		hb1.draw(win)
		hb2.draw(win, "#ff0000")
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
main()
