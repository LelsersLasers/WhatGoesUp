from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta

from classes import Vector, Hitbox # our classes


def calc_average(lst: list[float]) -> float:
	if len(lst) == 0: return 1
	return sum(lst)/len(lst)

def set_delta(time_0: float, time_1: float, deltas: list[float], target_fps: float, frame: int) -> tuple[float, float, float, int]:
	time_1 = time.perf_counter()
	if (frame > 20): deltas.append(target_fps/(1/(time_1 - time_0)))
	frame += 1
	time_0 = time.perf_counter()
	return calc_average(deltas), time_0, time_1, frame


def create_window() -> pygame.Surface:
	pygame.init()
	flags = pygame.SCALED | pygame.FULLSCREEN
	win = pygame.display.set_mode((1920, 1080), flags)
	x, y = win.get_size() # WHAT DOES THIS DO???
	size = (x, y * .8) # Or this?
	pygame.display.set_caption("TempName: v-0.01")
	return win


def handle_events() -> None:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

def handle_keys(keys_down: list[bool], delta: float, hb1: Hitbox) -> None:
	vec_move = Vector(0, 0)
	if keys_down[K_w]:
		vec_move.set_y(-10)
	elif keys_down[K_s]:
		vec_move.set_y(10)
	elif keys_down[K_a]:
		vec_move.set_x(-10)
	elif keys_down[K_d]:
		vec_move.set_x(10)
	vec_move = vec_move.scalar(delta)
	hb1.get_pt().apply(vec_move)

	if (keys_down[K_RCTRL] or keys_down[K_LCTRL]) and keys_down[K_q]:
		pygame.quit()
		quit()


def draw_welcome(win: pygame.Surface, hb_mouse: Hitbox) -> None:
	font = pygame.font.SysFont('Monospace', 30)
	surf_text = font.render("TEMP NAME", True, "#ff0000")
	win.blit(surf_text, (30, 30))
	hb_mouse.draw(win)


def draw_game(win: pygame.Surface, hb1: Hitbox, hb2: Hitbox, hb_mouse: Hitbox) -> None:
	win.fill("#fdf6e3")

	hb1.draw(win)
	hb2.draw(win, "#ff0000" if hb1.checkCollide(hb2) else "#0000ff")

	hb_mouse.draw(win)


def main():

	target_fps = 60
	deltas = []
	delta = 1.0 # relative to target_fps
	frame = 0

	screen = "welcome"
	game_status = True

	clock = pygame.time.Clock()
	time_0 = time.perf_counter()
	time_1 = time.perf_counter()

	win = create_window()

	hb1 = Hitbox(Vector(100, 100), 100, 100)
	hb2 = Hitbox(Vector(400, 400), 100, 100)

	hb_mouse = Hitbox(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5), 10, 10)

	while game_status:
		handle_events()
		handle_keys(pygame.key.get_pressed(), delta, hb1)

		hb_mouse.set_pt(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5))

		win.fill("#fdf6e3")
		if screen == "game": draw_game(win, hb1, hb2, hb_mouse)
		elif screen == "welcome": draw_welcome(win, hb_mouse)
		pygame.display.flip()

		clock.tick_busy_loop(target_fps)
		delta, time_0, time_1, frame = set_delta(time_0, time_1, deltas, target_fps, frame)

		
main()
