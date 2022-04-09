from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta

from classes import Vector, Hitbox, Player # our classes


def calc_average(lst: list[float]) -> float:
	if len(lst) == 0:
		return 1
	return sum(lst)/len(lst)

def set_delta(time_0: float, time_1: float, deltas: list[float], target_fps: float, frame: int) -> tuple[float, float, float, int]:
	time_1 = time.perf_counter()
	if (frame > 20):
		deltas.append(target_fps/(1/(time_1 - time_0)))
	frame += 1
	time_0 = time.perf_counter()
	return calc_average(deltas), time_0, time_1, frame


def create_window() -> pygame.Surface:
	pygame.init()
	flags = pygame.SCALED | pygame.FULLSCREEN
	win = pygame.display.set_mode((1920, 1080), flags)
	pygame.display.set_caption("TempName: v-0.01")
	return win


def handle_events() -> None:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()


def handle_keys(screen: str, player: Player, delta: float) -> str:
	keys_down = pygame.key.get_pressed()
	if (keys_down[K_RCTRL] or keys_down[K_LCTRL]) and keys_down[K_q]:
		pygame.quit()
		quit()
	elif screen == "welcome" and keys_down[K_RETURN]:
		return "game"
	elif screen == "game":
		player.handle_keys(keys_down, delta)
	return screen


def handle_mouse(screen: str, hb_mouse: Hitbox) -> str:
	hb_mouse.set_pt(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5))
	mouse_buttons_down = pygame.mouse.get_pressed()
	if mouse_buttons_down[0]:
		hb_mouse.set_color("#ff0000")
		if screen == "welcome":
			return "game"
	else:
		hb_mouse.set_color("#ff00ff")
	return screen


def draw_welcome(win: pygame.Surface, hb_mouse: Hitbox) -> None:
	font = pygame.font.SysFont('Monospace', 60)
	surf_text = font.render("TEMP NAME", True, "#ff0000")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	hb_mouse.draw(win)


def draw_game(win: pygame.Surface, hb1: Hitbox, hb2: Hitbox, player: Player, hb_mouse: Hitbox) -> None:
	win.fill("#fdf6e3")

	hb1.draw(win)
	hb2.set_color("#ff0000" if player.check_collide(hb2) else "#0000ff")
	hb2.draw(win)
	player.draw(win)

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
	hb2 = Hitbox(Vector(400, 400), 100, 100, "#0000ff")
	player = Player()

	hb_mouse = Hitbox(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5), 10, 10, "#ff00ff")

	while game_status:
		handle_events()
		screen = handle_keys(screen, player, delta)
		screen = handle_mouse(screen, hb_mouse)

		win.fill("#fdf6e3")
		if screen == "game":
			draw_game(win, hb1, hb2, player, hb_mouse)
		elif screen == "welcome":
			draw_welcome(win, hb_mouse)
		pygame.display.flip()

		clock.tick_busy_loop(target_fps)
		delta, time_0, time_1, frame = set_delta(time_0, time_1, deltas, target_fps, frame)
		print("FPS: %4.2f" % ((1/delta) * target_fps))


main()
