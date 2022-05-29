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
	# s.set_alpha(128)                # alpha level
	# s.fill((255,255,255))           # this fills the entire surface
	# windowSurface.blit(s, (0,0))    # (0,0) are the top-left coordinates


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
	elif screen == "game" and not player.get_is_alive():
		return "dead"
	elif screen == "game":
		player.handle_keys(keys_down, hb_mouse, delta, walls)
	elif screen == "dead" and keys_down[K_RETURN]:
		return "game"
	return screen

def handle_mouse(screen: str, hb_mouse: Hitbox) -> str:
	hb_mouse.set_pt(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5))
	mouse_buttons_down = pygame.mouse.get_pressed()
	if mouse_buttons_down[0]:
		hb_mouse.set_color("#ff0000")
		if screen == "welcome" or screen == "dead":
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
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	hb_mouse.draw(win)

def draw_dead(win: pygame.Surface, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float) -> None:
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	hb_mouse.draw(win)
	# Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
	rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
	rect.fill((158,157,155, 128))           # this fills the entire surface
	win.blit(rect, (0,0))    # (0,0) are the top-left coordinates
	font = pygame.font.SysFont('Monospace', 60)
	surf_text = font.render("YOU HAVE DIED", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	hb_mouse.draw(win)

def load_level(level: int) -> list[Surface]:
	if level == 1:
		return [
			# Surface(Vector(,), , , ),
			Surface(Vector(0, 800), 1920, 580, -.15),
			Surface(Vector(180, 780), 80, 20, -.15),
			Surface(Vector(290, 700), 80, 20, -.15),
			Surface(Vector(410, 670), 80, 20, -.15),
			Surface(Vector(510, 640), 80, 20, -.15),
			Surface(Vector(620, 610), 80, 20, -.15),
			Surface(Vector(730, 520), 80, 20, -.15),
			Surface(Vector(840, 470), 80, 20, -.15),
			Surface(Vector(1145, 570), 65, 20, -.2),
			Surface(Vector(1220, 480), 10, 40, -.2),
			Surface(Vector(1240, 600), 60, 20, -.2),
			Surface(Vector(1340, 560), 60, 20, -.2),
			Surface(Vector(1450, 410), 60, 20, -.15),
			Surface(Vector(1450, 290), 100, 20, -.15),
			Surface(Vector(1700, 290), 60, 20, -.15),
			Surface(Vector(1800, 190), 10, 60, -.15),
			Surface(Vector(1700, 190), 100, 20, -.15),
			Surface(Vector(1700, 100), 10, 90, -.15),
			Surface(Vector(1845, 290), 20, 20, -.15),
			Surface(Vector(1815, 300), 30, 10, -.3),
			Surface(Vector(1800, 110), 20, 100, -.15),
			Surface(Vector(1400, 110), 200, 20, -.15),
			Surface(Vector(1500, 20), 10, 63, -.15),
			Surface(Vector(1400, 0), 520, 20, -.15),
			Surface(Vector(600, 0), 120, 20, -.3),
			Surface(Vector(400, 0), 100, 20, -.15),
			Surface(Vector(150, 0), 150, 20, -.15),
			Surface(Vector(100, -100), 100, 20, -.15),
			Surface(Vector(180, -300), 20, 200, -.15),
			Surface(Vector(0, -200), 50, 20, -.15),
			Surface(Vector(0, -400), 200, 20, -.15),
			Surface(Vector(0, -600), 200, 200, -.15),
			Surface(Vector(0, -400), 20, 400, -.15),
			Surface(Vector(320, -450), 40, 20, -.15),
			Surface(Vector(1600, -450), 100, 20, -.35),
			Surface(Vector(1560, -350), 140, 20, -.25),
			Surface(Vector(1640, -560), 60, 20, -.2),
			Surface(Vector(900, -580), 80, 20, .15, "#00ffff"),
			Surface(Vector(1740, -725), 40, 200, -.15),
			Surface(Vector(1740, -1000), 40, 200, -.15),
			Surface(Vector(1760, -800), 20, 105, -.15),
			Surface(Vector(1650, -830), 20, 20, -.15),
			Surface(Vector(1430, -930), 50, 20, -.15),
			Surface(Vector(1400, -950), 30, 40, -.15),
			Surface(Vector(1005, -970), 90, 20, -.15),
			Surface(Vector(800, -1120), 700, 40, -.15),
			Surface(Vector(1200, -970), 70, 20, -.15),
			Surface(Vector(800, -970), 100, 75, -.15),
			Surface(Vector(800, -1100), 100, 75, -.15),
			Surface(Vector(720, -970), 30, 20, -.15),
			Surface(Vector(1480, -1220), 20, 100, -.15),
			Surface(Vector(1530, -1300), 20, 40, -.15),
			Surface(Vector(1590, -1400), 20, 40, -.15),
			Surface(Vector(1590, -1800), 20, 40, -.15),
			Surface(Vector(1650, -1500), 20, 40, -.15),
			Surface(Vector(1650, -1700), 20, 40, -.15),
			Surface(Vector(1750, -1600), 20, 40, -.15),
			Surface(Vector(1370, -1500), 20, 40, -.15),
			Surface(Vector(1200, -1340), 60, 20, -.15),
			Surface(Vector(400, -1340), 120, 20, -.15),
			Surface(Vector(300, -1500), 15, 40, -.15),
			Surface(Vector(200, -1700), 15, 40, -.15),
			Surface(Vector(200, -1800), 15, 40, -.15),
			Surface(Vector(300, -1600), 15, 40, -.15),
			Surface(Vector(400, -2800), 20, 900, -.15),
			Surface(Vector(195, -1970), 10, 25, -.15),
			Surface(Vector(350, -2020), 50, 20, -.15),
			Surface(Vector(300, -2170), 10, 15, -.15),
			Surface(Vector(0, -2220), 50, 20, -.15),
			Surface(Vector(350, -2220), 50, 20, -.15),
			Surface(Vector(100, -2320), 10, 15, -.15),
			Surface(Vector(0, -2420), 50, 20, -.15),
			Surface(Vector(350, -2460), 50, 20, -.15),
			Surface(Vector(300, -2570), 10, 15, -.15),
			Surface(Vector(175, -2720), 50, 15, -.15),
			Surface(Vector(330, -2850), 90, 50, -.15),
			Surface(Vector(950, -2560), 300, 20, .11, "#00ffff"),
			Surface(Vector(1650, -2580), 130, 20, -.15),
			Surface(Vector(1650, -2880), 20, 250, -.15),
			Surface(Vector(1650, -2680), 40, 20, -.15),
			Surface(Vector(1750, -2780), 40, 20, -.15),
			Surface(Vector(1410, -2980), 100, 20, -.15),
			Surface(Vector(1250, -2977), 100, 20, -.15),
			Surface(Vector(1050, -3100), 470, 20, -.15),
			Surface(Vector(1380, -3100), 30, 85, -.15),
			Surface(Vector(1500, -3300), 20, 200, -.15),
			Surface(Vector(1210, -2980), 10, 20, -.15),
			Surface(Vector(1110, -2980), 10, 20, -.15),
			Surface(Vector(1000, -2980), 10, 20, -.15),
			Surface(Vector(1050, -3300), 400, 20, -.15),
			Surface(Vector(1080, -3200), 10, 100, -.15, "#ff0000", True),
			Surface(Vector(1280, -3310), 30, 180, -.15, "#ff0000", True),
			Surface(Vector(1380, -3200), 20, 100, -.15, "#ff0000", True),
			Surface(Vector(1440, -3220), 20, 10, -.15),
			# Side walls
			Surface(Vector(0, -4000), 10, 5080, -.1),
			Surface(Vector(1910, -4000), 10, 5080, -.1),
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
			# essentially reset the game
			# Add a death screen
		if screen == "dead":
			can_respawn = True
		else:
			can_respawn = False
		handle_events()
		screen = handle_keys(screen, player, hb_mouse, delta, walls)
		screen = handle_mouse(screen, hb_mouse)

		win.fill("#fdf6e3")
		if screen == "game":
			if can_respawn:
				player = Player()
				walls = load_level(1)
			draw_game(win, player, walls, hb_mouse, delta)
		elif screen == "welcome":
			draw_welcome(win, hb_mouse)
		elif screen == "dead":
			draw_dead(win, player, walls, hb_mouse, delta)
		pygame.display.flip()


		# clock.tick_busy_loop(60)
		delta, time_0, time_1, frame = set_delta(time_0, time_1, deltas, frame)
		# print(delta)
		print("FPS: %4.2f" % (1/delta))


main()
