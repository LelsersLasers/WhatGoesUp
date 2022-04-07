from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta

from classes import Vector, Hitbox # our classes


def calc_average(lst: list[float]) -> float:
	return sum(lst) / len(lst)

def set_delta(time_0: float, time_1: float, deltas: list[float], target_fps: float) -> tuple[float, int, int]:
	time_1 = time.process_time_ns()
	last_loop_time = (time_1 - time_0) / 1_000_000_000 # convert to sec
	if (last_loop_time == 0): last_loop_time = 1 / target_fps # BUG: solve why it is 0 sometimes
	last_fps = 1 / last_loop_time
	last_delta = last_fps / target_fps
	deltas.append(last_delta)
	time_0 = time.process_time_ns()
	return calc_average(deltas), time_0, time_1

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
	deltas = []
	delta = 1.0 # relative to target_fps

	win = createWindow()
	clock = pygame.time.Clock()
	time_0 = time.process_time_ns()
	time_1 = time.process_time_ns()
	print(time_0)

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
		clock.tick_busy_loop(target_fps)

		delta, time_0, time_1 = set_delta(time_0, time_1, deltas, target_fps)
		print(delta)

		
main()
