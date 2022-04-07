from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta


from classes import Vector, Hitbox # our classes

def createWindow() -> pygame.Surface:
	pygame.init()
	# win = pygame.display.set_mode((600, 600), FULLSCREEN)
	win = pygame.display.set_mode((800, 800))
	x, y = win.get_size()
	size = (x, y * .8) # WHAT DOES THIS DO???
	pygame.display.set_caption("TempName: v-0.01")
	return win


def main():

	target_fps = 60
	delta = 1.0 # relative to target_fps

	win = createWindow()
	clock = pygame.time.Clock()
	time_0 = time.process_time_ns()
	time_1 = time.process_time_ns()

	hb1 = Hitbox(Vector(100, 100), 100, 100)
	hb2 = Hitbox(Vector(400, 400), 100, 100)

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

		time_1 = time.process_time_ns()
		loop_time_1 = clock.tick_busy_loop(target_fps)
		real_fps_1 = 1000/loop_time_1
		print(loop_time_1, real_fps_1)

		time_1 = time.process_time()
		loop_time_2 = (time_1 - time_0)
		if loop_time_2 == 0:
			print("000000000000000000000")
		else:
			real_fps_2 = 1 / loop_time_2
			print("1:", loop_time_2, real_fps_2, "2:", loop_time_1, real_fps_1)
		time_0 = time.process_time()

		
main()
