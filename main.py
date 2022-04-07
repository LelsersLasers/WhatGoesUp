from __future__ import annotations # for type hints

import pygame # graphics library
from pygame.locals import * # used for keyboard input (ex: 'K_w')

from classes import Vector, Hitbox # our classes

target_FPS = 60

def createWindow() -> pygame.Surface:
	pygame.init()
	# win = pygame.display.set_mode((600, 600), FULLSCREEN)
	win = pygame.display.set_mode((800, 800))
	x, y = win.get_size()
	size = (x, y * .8) # WHAT DOES THIS DO???
	pygame.display.set_caption("TempName: v-0.01")
	return win


def main():
	win = createWindow()
	hb1 = Hitbox(Vector(100, 100), 100, 100)
	hb2 = Hitbox(Vector(400, 400), 100, 100)

	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		keys_down = pygame.key.get_pressed()
		if keys_down[K_w]:
			hb1.get_pt().set_y(hb1.get_pt().get_y() - 4)
		elif keys_down[K_s]:
			hb1.get_pt().set_y(hb1.get_pt().get_y() + 4)
		elif keys_down[K_a]:
			hb1.get_pt().set_x(hb1.get_pt().get_x() - 4)
		elif keys_down[K_d]:
			hb1.get_pt().set_x(hb1.get_pt().get_x() + 4)


		win.fill("#000000")

		color = "#0000ff"
		if hb1.checkCollide(hb2):
			color = "#ff0000"

		hb1.draw(win)
		hb2.draw(win, color)

		pygame.display.flip()
		clock.tick_busy_loop(target_FPS)

		
main()
