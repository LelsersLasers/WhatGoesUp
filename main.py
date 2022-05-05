from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta

from classes import Vector, Hitbox, HitboxPart, AdvancedHitbox, Player, Surface # our classes


def calc_average(lst: list[float]) -> float:
	if len(lst) == 0:
		return 1
	return sum(lst)/len(lst)

def set_delta(time_0: float, time_1: float, deltas: list[float], frame: int) -> tuple[float, float, float, int]:
	time_1 = time.perf_counter()
	if (frame > 20):
		deltas.append(time_1 - time_0)
	frame += 1
	time_0 = time.perf_counter()
	return calc_average(deltas), time_0, time_1, frame


def create_window() -> pygame.Surface:
	pygame.init()
	flags = pygame.SCALED | pygame.FULLSCREEN
	win = pygame.display.set_mode((1920, 1080), flags)
	pygame.display.set_caption("TempName: v-0.94")
	return win

def handle_events() -> None:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()


def handle_keys(screen: str, player: Player, hb_mouse, delta: float, walls) -> str:
	keys_down = pygame.key.get_pressed()
	if (keys_down[K_RCTRL] or keys_down[K_LCTRL]) and keys_down[K_q]:
		pygame.quit()
		quit()
	elif screen == "welcome" and keys_down[K_RETURN]:
		return "game"
	elif screen == "game":
		player.handle_keys(keys_down, hb_mouse, delta, walls)
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


def draw_game(win: pygame.Surface, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float) -> None:
	win.fill("#fdf6e3")
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	hb_mouse.draw(win)


def main():

	deltas = []
	delta = 0.017 # second since last frame
	frame = 0

	screen = "welcome"
	game_status = True

	clock = pygame.time.Clock()
	time_0 = time.perf_counter()
	time_1 = time.perf_counter()

	win = create_window()

	player = Player()
	walls = [
		Surface(Vector(0, 1000), 1920, 100, .95, "#000000"),
		Surface(Vector(0, 0), 10, 1080, .95, "#000000"),
		Surface(Vector(1910, 0), 10, 1080, .95, "#000000"),
		Surface(Vector(180, 980), 80, 20, .95, "#000000"),
		Surface(Vector(295, 900), 80, 20, .95, "#000000"),
		Surface(Vector(410, 870), 80, 20, .95, "#000000"),
		Surface(Vector(510, 840), 80, 20, .95, "#000000"),
		Surface(Vector(620, 810), 80, 20, .95, "#000000"),
		Surface(Vector(730, 720), 80, 20, .95, "#000000"),
		Surface(Vector(840, 670), 80, 20, .8, "#000000"),
		Surface(Vector(1150, 770), 60, 20, .95, "#000000"),
		Surface(Vector(1200, 760), 10, 10, .95, "#000000"),
		Surface(Vector(1240, 800), 60, 20, .95, "#000000"),
		Surface(Vector(1340, 760), 60, 20, .95, "#000000"),
		Surface(Vector(1440, 660), 60, 20, .95, "#000000"),
		Surface(Vector(1540, 575), 40, 200, .89, "#000000"),
		Surface(Vector(1540, 350), 40, 150, .95, "#000000"),
		Surface(Vector(1560, 500), 20, 75, .95, "#000000"),


	]
	hb_mouse = Hitbox(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5), 10, 10, "#ff00ff")

	while game_status:
		handle_events()
		screen = handle_keys(screen, player, hb_mouse, delta, walls)
		screen = handle_mouse(screen, hb_mouse)

		win.fill("#fdf6e3")
		if screen == "game":
			draw_game(win, player, walls, hb_mouse, delta)
		elif screen == "welcome":
			draw_welcome(win, hb_mouse)
		pygame.display.flip()


		# clock.tick_busy_loop(60)
		delta, time_0, time_1, frame = set_delta(time_0, time_1, deltas, frame)
		# print("FPS: %4.2f" % (1/delta))


main()
