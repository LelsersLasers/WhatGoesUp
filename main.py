from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta
import datetime # for timer

from classes import Vector, Hitbox, HitboxPart, AdvancedHitbox, Player, Surface, Button


def calc_average(lst: list[float]) -> float:
	if len(lst) == 0:
		return 1/100
	return sum(lst)/len(lst)

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
	elif (screen == "game" or screen == "dead") and keys_down[K_ESCAPE]:
		return "pause"
	elif screen == "game" and not player.get_is_alive():
		return "dead"
	elif screen == "game":
		player.handle_keys(keys_down, hb_mouse, delta, walls)
		if player.get_is_finished():
			return "finished"
	elif screen == "dead" and keys_down[K_RETURN]:
		return "game"
	return screen

def handle_mouse(screen: str, hb_mouse: Hitbox, buttons: list[Button]) -> str:
	hb_mouse.set_pt(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5))
	mouse_buttons_down = pygame.mouse.get_pressed()
	if mouse_buttons_down[0]:
		hb_mouse.set_color("#ff0000")
		for button in buttons:
			print(button)
			if hb_mouse.check_collide(button):
				print("collide")
				if button.get_text() == "PLAY" or button.get_text() == "PLAY AGAIN" or button.get_text() == "RETURN":
					return "game"
				elif button.get_text() == "BACK TO MAIN MENU" or button.get_text() == "MAIN MENU":
					return "welcome"
	else:
		hb_mouse.set_color("#ff00ff")
	return screen


def draw_welcome(win: pygame.Surface, hb_mouse: Hitbox, buttons: list[Button]) -> None:
	win.fill("#fdf6e3")
	font = pygame.font.SysFont('Monospace', 60)
	surf_text = font.render("WHAT GOES UP...", True, "#ff0000")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	for button in buttons:
		button.draw(win)
	hb_mouse.draw(win)

def draw_game(win: pygame.Surface, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, elapsed_time: time) -> None:
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	# Elapsed time
	font = pygame.font.SysFont('Monospace', 20) # is it bad to always re-create the font?
	time = str(elapsed_time).split(".")
	surf_time_text = font.render(str(time[0]), True, "#ffffff")
	font_rect = (0, 0, surf_time_text.get_width() + win.get_width() * .05, surf_time_text.get_height() + 20)
	pygame.draw.rect(win, "#000000", font_rect)
	win.blit(surf_time_text, ((win.get_width() * 0.025, 10)))

	# Delta flutter visualization
	max_width_ratio = font_rect[2]/(1/200)
	delta_rec = (0, font_rect[3], delta * max_width_ratio, font_rect[3] * 0.5)
	pygame.draw.rect(win, "#00ff00", delta_rec)
	pygame.draw.rect(win, "#ffffff", delta_rec, 2)

	font = pygame.font.SysFont('Monospace', 12) # is it bad to always re-create the font?
	surf_delta_text = font.render("Delta: %.3f" % delta, True, "#000000")
	win.blit(surf_delta_text, ((win.get_width() * 0.005, 46)))


	hb_mouse.draw(win)

def draw_dead(win: pygame.Surface, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, buttons: list[Button]) -> None:
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	hb_mouse.draw(win)
	# Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
	rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
	rect.fill((0,0,0, 128))           # this fills the entire surface
	win.blit(rect, (0,0))    # (0,0) are the top-left coordinates
	font = pygame.font.SysFont('Monospace', 60)
	surf_text = font.render("YOU HAVE DIED", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	for button in buttons:
		button.draw(win)
	hb_mouse.draw(win)

def draw_pause(win: pygame.Surface, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, buttons: list[Button]) -> None:
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	hb_mouse.draw(win)
	# Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
	rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
	rect.fill((0,0,0, 128))           # this fills the entire surface
	win.blit(rect, (0,0))    # (0,0) are the top-left coordinates
	font = pygame.font.SysFont('Monospace', 60)
	surf_text = font.render("OPTIONS", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	for button in buttons:
		button.draw(win)
	hb_mouse.draw(win)

def draw_finished(win: pygame.Surface, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, buttons: list[Button]) -> None:
	# win.fill("#3973fa")
	win.fill("#fdf6e3")
	font = pygame.font.SysFont('Monospace', 60)
	surf_text = font.render("YOU FINISHED", True, "#ff0000")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	for button in buttons:
		button.draw(win)
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
			Surface(Vector(380, -3360), 120, 20, -.2),
			Surface(Vector(0, -3460), 100, 20, -.15),
			Surface(Vector(380, -3560), 120, 20, -.2),
			Surface(Vector(600, -3700), 120, 20, -.15),
			Surface(Vector(1400, -3750), 150, 20, -.15),
			Surface(Vector(1600, -3850), 10, 25, -.15),
			Surface(Vector(1700, -4000), 10, 25, -.15),
			Surface(Vector(1800, -4150), 10, 25, -.15),
			Surface(Vector(1700, -4250), 10, 25, -.15),
			Surface(Vector(1550, -4350), 10, 25, -.15),
			Surface(Vector(1550, -4500), 10, 25, -.15),
			Surface(Vector(1450, -4550), 10, 25, -.15),
			Surface(Vector(1300, -4600), 10, 25, -.1),
			Surface(Vector(1200, -4700), 10, 25, -.1),
			Surface(Vector(1000, -4550), 10, 25, -.1),
			Surface(Vector(900, -4600), 10, 25, -.1),
			Surface(Vector(900, -4750), 10, 25, -.1),
			Surface(Vector(900, -4900), 10, 25, -.1),
			Surface(Vector(1050, -4900), 400, 30, -.15),
			Surface(Vector(1200, -5025), 30, 125, -.15, "#ff0000", True),
			# Side walls
			Surface(Vector(0, -5500), 10, 6580, -.1),
			Surface(Vector(1910, -5500), 10, 6580, -.1),
			Surface(Vector(0, -6000), 1920, 500, -.1),
			Surface(Vector(1650, -5050), 50, 50, -.15, "#888800", False, True),
		]
	else:
		return []

def save_map(walls: list[Surface]) -> None:
	f_name = input("File Name: ")
	for wall in walls:
		pos = "{},{},{},{},{},{},{}\n"
		f.write(pos.format(wall.get_pt().get_x(), wall.get_pt().get_y(), wall.get_w(), wall.get_h(), wall.get_friction(), wall.get_can_kill(), wall.get_is_finish()))
	f.close()

def load_map(map_num: int) -> list[Surface]:
	if map_num == 0:
		f = open("map_saves/map_1", "r")
		walls = []
		for line in f:
			line.strip()
			stats = line.split(",")
			# print(stats)
			if stats[5]:
				color = "#ff0000"
			elif stats[6]:
				color = "#999900"
			else:
				color = "#000000"
			wall = Surface(Vector(stats[0], stats[1]), stats[2], stats[3], stats[4], color, stats[5], stats[6])
			walls.append(wall)
	return walls
def create_buttons(win: pygame.Surface):
	font = pygame.font.SysFont('Monospace', 40)
	surf_text = font.render("PLAY", True, "#000000")
	play_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.35), surf_text.get_width(), surf_text.get_height(), "PLAY", False)
	dead_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.35), surf_text.get_width(), surf_text.get_height(), "PLAY", False, "#ffffff")
	surf_text = font.render("PLAY AGAIN", True, "#000000")
	f_play_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.35), surf_text.get_width(), surf_text.get_height(), "PLAY AGAIN", False)
	surf_text = font.render("BACK TO MAIN MENU", True, "#000000")
	menu_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.6), surf_text.get_width(), surf_text.get_height(), "BACK TO MAIN MENU", False)
	d_menu_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.6), surf_text.get_width(), surf_text.get_height(), "BACK TO MAIN MENU", False, "#ffffff")
	surf_text = font.render("RETURN", True, "#000000")
	return_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.35), surf_text.get_width(), surf_text.get_height(), "RETURN", False, "#ffffff")
	surf_text = font.render("MAIN MENU", True, "#000000")
	p_menu_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.65), surf_text.get_width(), surf_text.get_height(), "MAIN MENU", False, "#ffffff")
	surf_text = font.render("SETTINGS", True, "#000000")
	settings_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.5), surf_text.get_width(), surf_text.get_height(), "SETTINGS", False, "#ffffff")

	welc_buttons = [play_button]
	fin_buttons = [f_play_button, menu_button]
	dead_buttons = [dead_button, d_menu_button]
	pause_buttons = [return_button, p_menu_button, settings_button]
	buttons = []

	return buttons, welc_buttons, fin_buttons, dead_buttons, pause_buttons

def main():

	delta = 0.017 # second since last frame
	last_frame = time.time()

	screen = "welcome"
	game_status = True

	# clock = pygame.time.Clock()
	start_time = datetime.datetime.now()

	win = create_window()

	player = Player()
	walls = load_map(0)
	# save_map(walls)
	hb_mouse = Hitbox(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5), 10, 10, "#ff00ff")
	buttons, welc_buttons, fin_buttons, dead_buttons, pause_buttons = create_buttons(win)

	while game_status:
		delta = time.time() - last_frame
		last_frame = time.time()
		if screen == "game" or screen == "pause":
			can_respawn = False
		else:
			can_respawn = True
		handle_events()
		screen = handle_keys(screen, player, hb_mouse, delta, walls)
		if screen == "welcome":
			screen = handle_mouse(screen, hb_mouse, welc_buttons)
		elif screen == "finished":
			screen = handle_mouse(screen, hb_mouse, fin_buttons)
		elif screen == "dead":
			screen = handle_mouse(screen, hb_mouse, dead_buttons)
		elif screen == "pause":
			# print("yes")
			screen = handle_mouse(screen, hb_mouse, pause_buttons)
		else:
			screen = handle_mouse(screen, hb_mouse, buttons)

		if screen == "game":
			if can_respawn:
				player = Player()
				walls = load_level(1)
			elapsed_time = datetime.datetime.now() - start_time
			# print(datetime.datetime.now())
			draw_game(win, player, walls, hb_mouse, delta, elapsed_time)
		elif screen == "welcome":
			draw_welcome(win, hb_mouse, welc_buttons)
		elif screen == "dead":
			start_time = datetime.datetime.now() - elapsed_time
			draw_dead(win, player, walls, hb_mouse, delta, dead_buttons)
		elif screen == "pause":
			start_time = datetime.datetime.now() - elapsed_time
			draw_pause(win, player, walls, hb_mouse, delta, pause_buttons)
		elif screen == "finished":
			draw_finished(win, player, walls, hb_mouse, delta, fin_buttons)
		pygame.display.flip()


		# clock.tick_busy_loop(300)

		print("Delta: %1.3f\tFPS: %4.2f" % (delta, 1/delta))


main()
