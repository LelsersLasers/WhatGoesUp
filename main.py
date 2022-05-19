from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta

from classes import Vector, Hitbox, HitboxPart, AdvancedHitbox, Player, Surface # our classes


def calc_average(lst: list[float]) -> float:
	if len(lst) == 0:
		return 1/100
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
	win = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
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

def load_level(level: int) -> list[Surface]:
	if level == 1:
		return [
			# Surface(Vector(,), , , ),
			Surface(Vector(0, 800), 1920, 580, .9),
			Surface(Vector(180, 780), 80, 20, .9),
			Surface(Vector(290, 700), 80, 20, .9),
			Surface(Vector(410, 670), 80, 20, .9),
			Surface(Vector(510, 640), 80, 20, .9),
			Surface(Vector(620, 610), 80, 20, .9),
			Surface(Vector(730, 520), 80, 20, .9),
			Surface(Vector(840, 470), 80, 20, .9),
			Surface(Vector(1145, 570), 65, 20, .85),
			Surface(Vector(1220, 480), 10, 40, .85),
			Surface(Vector(1240, 600), 60, 20, .85),
			Surface(Vector(1340, 560), 60, 20, .85),
			Surface(Vector(1450, 410), 60, 20, .9),
			Surface(Vector(1450, 290), 60, 20, .9),
			Surface(Vector(1700, 290), 60, 20, .9),
			Surface(Vector(1800, 190), 10, 60, .9),
			Surface(Vector(1700, 190), 100, 20, .9),
			Surface(Vector(1700, 100), 10, 90, .9),
			Surface(Vector(1845, 290), 20, 20, .9),
			Surface(Vector(1815, 300), 30, 10, .7),
			Surface(Vector(1800, 110), 20, 100, .9),
			Surface(Vector(1400, 110), 200, 20, .9),
			Surface(Vector(1500, 20), 10, 63, .9),
			Surface(Vector(1400, 0), 520, 20, .9),
			Surface(Vector(600, 0), 120, 20, .7),
			Surface(Vector(400, 0), 100, 20, .9),
			Surface(Vector(150, 0), 150, 20, .9),
			Surface(Vector(100, -100), 100, 20, .9),
			Surface(Vector(180, -300), 20, 200, .9),
			Surface(Vector(0, -200), 50, 20, .9),
			Surface(Vector(0, -400), 200, 20, .9),
			Surface(Vector(0, -600), 200, 200, .9),
			Surface(Vector(0, -400), 20, 400, .9),
			Surface(Vector(350, -450), 40, 20, .9),
			Surface(Vector(1600, -450), 100, 20, .85),
			Surface(Vector(1620, -560), 80, 20, .9),
			Surface(Vector(1740, -745), 40, 200, .9),
			Surface(Vector(1740, -1000), 40, 200, .9),
			Surface(Vector(1760, -800), 20, 85, .9),
			Surface(Vector(1650, -840), 20, 20, .9),
			# Surface(Vector(1470, 200), 50, 20, .9),
			# Surface(Vector(1445, 180), 30, 40, .9),
			# Surface(Vector(1005, 175), 90, 20, .9),
			# Surface(Vector(0, 0), 700, 40, .9),
			# Surface(Vector(800, 0), 1120, 40, .9),
			# Surface(Vector(840, 150), 70, 20, .9),
			# Surface(Vector(800, 0), 100, 75, .9),
			# Surface(Vector(720, 150), 30, 20, .9),
			# end of first section (no slid jumps yet)
			# Surface(Vector(680, -500), 20, 400, .9),
			# Surface(Vector(680, -40), 20, 40, .9),
			Surface(Vector(0, -2000), 10, 3080, .9),
			Surface(Vector(1910, -2000), 10, 3080, .9),
		]
	else:
		return []

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
	walls = load_level(1)
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
		# print(delta)
		print("FPS: %4.2f" % (1/delta))


main()
