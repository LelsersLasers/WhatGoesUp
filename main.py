from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import time # for fps/delta
import datetime # for timer
import sys

from classes import DownPress, Vector, Hitbox, HitboxPart, AdvancedHitbox, User, Player, Surface, Teleporter, Button, ToggleButton, Map

def create_window() -> pygame.Surface:
	pygame.init()
	win = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
	pygame.display.set_caption("TempName: v-0.94")
	pygame.mouse.set_cursor(*pygame.cursors.tri_left)
	return win
	# s.set_alpha(128)                # alpha level
	# s.fill((255,255,255))           # this fills the entire surface
	# windowSurface.blit(s, (0,0))    # (0,0) are the top-left coordinates

def create_fonts() -> list[pygame.Font]:
	fonts = []
	font_1 = pygame.font.SysFont('calibri', 80)
	# font_1.set_bold(True)
	font_2 = pygame.font.SysFont('calibri', 50)
	# font_2.set_bold(True)
	font_3 = pygame.font.SysFont('calibri', 60)
	# font_3.set_bold(True)
	fonts.append(font_1)
	fonts.append(font_2)
	fonts.append(font_3)

	return fonts

def handle_events(user) -> None:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_user(user)
			pygame.quit()
			sys.exit()
			quit()

def handle_keys(screen: str, player: Player, hb_mouse, delta: float, walls, teleporters, elapsed_time, times, current_map, deaths, keys_down, escape_down) -> str:
	if (keys_down[K_RCTRL] or keys_down[K_LCTRL]) and keys_down[K_q]:
		pygame.quit()
		sys.exit()
		quit()
	if keys_down[K_ESCAPE] and escape_down.down(True):
		"""
		if keys_down[self.user.jump] and self.get_is_grounded() and not self.get_jumped_while_sliding():
			self.set_space_was_down(False)
		elif keys_down[self.user.jump] and self.get_space_was_down():
			self.set_space_was_down(False)
		elif not keys_down[self.user.jump] and not self.get_space_was_down():
			self.set_space_was_down(True)
		"""
		if screen == "game" or screen == "dead" or screen == "settings_game":
			return "pause"
		elif screen == "pause" and player.get_is_alive():
			return "game"
		elif screen == "pause" and not player.get_is_alive():
			return "dead"
		elif screen == "welcome":
			return "exit"
		elif screen == "mechanics" or screen == "settings" or screen == "selc_leaderboard" or screen == "selection":
			return "welcome"
		elif screen == "leaderboard":
			return "selc_leaderboard"
	elif not keys_down[K_ESCAPE]:
		escape_down.down(False)
	if screen == "game" and not player.get_is_alive():
		deaths[0] += 1
		return "dead"
	elif screen == "game":
		player.handle_keys(keys_down, hb_mouse, delta, walls, teleporters)
		if player.get_is_finished():
			if len(times) > 0 and str(elapsed_time) < times[len(times) - 1]:
				pos = 0
				for i in range(len(times)):
					if str(elapsed_time) <= times[i]:
						pos = i
						break
				times.insert(pos, str(elapsed_time))
				if len(times) > 10:
					times.pop()
			else:
				times = [elapsed_time]
			save_times(times, str(current_map))
			return "finished"
	elif screen == "dead" and keys_down[K_RETURN]:
		return "respawn"
	return screen

def handle_mouse(screen: str, hb_mouse: Hitbox, buttons: list[Button], was_down: bool, mouse_buttons_down) -> str:
	hb_mouse.set_pt(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5))
	if mouse_buttons_down[0]:
		# hb_mouse.set_color("#ff0000")
		for button in buttons:
			# print(button)
			if hb_mouse.check_collide(button) and not was_down:
				if not button.toggle:
					# print("collide", button, button.get_text(), button.get_next_loc())
					# print(screen == "selc_leaderboard" and button.get_next_loc() != "welcome" and button.get_next_loc() != "exit")
					if screen == "selc_leaderboard" and button.get_next_loc() != "welcome" and button.get_next_loc() != "exit":
						next_loc = "leaderboard:" + str(button.get_next_loc())
					else:
						next_loc = button.get_next_loc()
				else:
					button.value = not button.value
					button.user.settings[button.setting] = button.value
					save_user(button.user)
					if button.value:
						color = button.on_color
					else:
						color = button.off_color
					button.set_color(color)
					# print(button.user.settings[button.setting])
					next_loc = button.get_next_loc()
				return next_loc, True
	else:
		was_down = False
	# 	hb_mouse.set_color("#ff00ff")
	return screen, was_down

def handle_inputs(win, font, input_rects, actives, user_texts, input_colors, color_passive, color_active, user, hb_mouse, was_down, keys_down, mouse_buttons_down, extra_keys):
	for i in range(4):
		# print(i)
		input_rect = input_rects[i]
		color = input_colors[i]
		if mouse_buttons_down[0]:
			# print("yes")
			# print(hb_mouse.check_collide(input_rect), i)
			if hb_mouse.check_collide(input_rect):
				# print(input_rect)
				actives[i] = True
				user_texts[i] = ''
				# print("yes")
				input_rect.set_color(color_active)
			elif not hb_mouse.check_collide(input_rect):
				actives[i] = False
				# print(user.settings[i])
				user_texts[i] = pygame.key.name(int(user.settings[i]))
				# print("no")
				input_rect.set_color(color_passive)
		# print(actives)
		if actives[i]:
			# for event in pygame.event.get():
			# print(i)
			if keys_down[K_BACKSPACE] == 1:
				# print("delete")
				user_texts[i] = user_texts[i][:-1]
			elif keys_down[K_RETURN] == 1:
				# print("enter")
				if user_texts[i] != '':
					# print(user_texts[i])
					valid = True
					for setting in user.settings:
						if pygame.key.key_code(user_texts[i]) == setting:
							valid = False
					if pygame.key.key_code(user_texts[i]) == user.settings[i]:
						actives[i] = False
						input_rect.set_color(color_passive)
						user_texts[i] = pygame.key.name(int(user.settings[i]))
					elif valid:
						user.set_setting(i, pygame.key.key_code(user_texts[i]))
						save_user(user)
						actives[i] = False
						input_rect.set_color(color_passive)
				else:
					user_texts[i] = pygame.key.name(int(user.settings[i]))
			else:
				# print("input")
				key = ''
				# print(keys_down)
				for K_key in extra_keys:
					if keys_down[K_key] == 1:
						key = pygame.key.name(K_key)
						# code = pygame.key.key_code(key)
						# print(key)
						user_texts[i] = key
						break
				for index in range(len(keys_down)):
					# print(keys_down[i])
					if keys_down[index] == 1:
						key = pygame.key.name(index)
						# code = pygame.key.key_code(key)
						# print(key)
						user_texts[i] = key
						break
						# print(pygame.key.name(index))
				# print(key, code, index)

def draw_welcome(win: pygame.Surface, font: pygame.font, hb_mouse: Hitbox, buttons: list[Button]) -> None:
	# 60 font
	win.fill("#6fcae8")
	surf_text = font.render("WHAT GOES UP...", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	for button in buttons:
		button.draw(win)
	# hb_mouse.draw(win)

def draw_selection(win: pygame.Surface, font: pygame.font, hb_mouse: Hitbox, buttons: list[Button]) -> None:
	# 60 font
	win.fill("#6fcae8")
	surf_text = font.render("MAP SELECTION", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 200))

	for button in buttons:
		button.draw(win)
	# hb_mouse.draw(win)

def draw_challenge(win: pygame.Surface, font: pygame.font, hb_mouse: Hitbox, buttons: list[Button]) -> None:
	win.fill("#6fcae8")
	surf_text = font.render("CHALLENGES", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 200))

	for button in buttons:
		button.draw(win)

def draw_game(win: pygame.Surface, font: pygame.font, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, elapsed_time: time) -> None:
	# 30 font
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		# print(wall)
		wall.draw(win)
	player.draw(win)

	# Elapsed time
	surf_time_text = font.render("Time: " + str(elapsed_time), True, "#ffffff")
	fps = 1/delta
	surf_fps_text = font.render("FPS: %4.0f" % fps, True, "#ffffff")
	height = surf_time_text.get_height() + surf_fps_text.get_height() + 40
	font_rect = (0, 0, surf_time_text.get_width() + win.get_width() * .075, height)
	pygame.draw.rect(win, "#000000", font_rect)
	win.blit(surf_time_text, ((win.get_width() * 0.0375, 10)))
	win.blit(surf_fps_text, ((win.get_width() * 0.0375, 50)))


	# hb_mouse.draw(win)

def draw_dead(win: pygame.Surface, font: pygame.font, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, buttons: list[Button], deaths) -> None:
	# 60 font
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	# hb_mouse.draw(win)
	# Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
	rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
	rect.fill((0,0,0, 128))           # this fills the entire surface
	win.blit(rect, (0,0))    # (0,0) are the top-left coordinates
	surf_text = font.render("YOU HAVE DIED", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	text = "Deaths: %i" % deaths[0]
	surf_text = font.render(text, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 300))
	for button in buttons:
		button.draw(win)
	# hb_mouse.draw(win)

def draw_pause(win: pygame.Surface, font: pygame.font, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, buttons: list[Button]) -> None:
	# 60 font
	win.fill("#fdf6e3")
	# use pygame.Surface.scroll for when background is an image
	for wall in walls:
		wall.draw(win)
	player.draw(win)

	# hb_mouse.draw(win)
	# Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
	rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
	rect.fill((0,0,0, 128))           # this fills the entire surface
	win.blit(rect, (0,0))    # (0,0) are the top-left coordinates
	surf_text = font.render("OPTIONS", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	for button in buttons:
		button.draw(win)
	# hb_mouse.draw(win)

def draw_finished(win: pygame.Surface, font: pygame.font, player: Player, walls: list[Surface], hb_mouse: Hitbox, delta: float, buttons: list[Button], elapsed_time) -> None:
	# 60 font
	# win.fill("#3973fa")
	win.fill("#6fcae8")
	surf_text = font.render("YOU FINISHED", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	surf_text = font.render("Time Taken:", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 200))

	times = str(elapsed_time).split(":")
	if not int(times[0]) == 0:
		 time = str(elapsed_time) + " hours"
	elif not int(times[1]) == 0:
		time = str(times[1]) + ":" + str(times[2]) + " minutes"
	else:
		time = str(times[2]) + " seconds"
	surf_text = font.render(time, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 300))
	for button in buttons:
		button.draw(win)
	# hb_mouse.draw(win)

def draw_selc_leaderboard(win, font, buttons):
	win.fill("#6fcae8")
	surf_text = font.render("LEADERBOARDS", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	surf_text = font.render("CHALLENGES", True, "#ffffff")
	win.blit(surf_text, (win.get_width() / 20, 250))
	surf_text = font.render("MAPS", True, "#ffffff")
	win.blit(surf_text, (win.get_width() / 2, 250))

	for button in buttons:
		button.draw(win)

def draw_leaderboard(win, fonts, times, name, buttons):
	win.fill("#6fcae8")
	surf_text = fonts[0].render(name, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))

	for i in range(len(times)):
		surf_text = fonts[1].render("%d) %s" % (i + 1, times[i]), True, "#ffffff")
		win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 200 + ((surf_text.get_height() + 30) * i)))
	for button in buttons:
 		button.draw(win)

def draw_mechanics(win, fonts, buttons, user):
	win.fill("#6fcae8")
	surf_text = fonts[0].render("CONTROLS", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))

	l1 = "Walk Right: %s" % pygame.key.name(user.settings[0])
	l2 = "Walk Left: %s" % pygame.key.name(user.settings[1])
	l3 = "Jump: %s" % pygame.key.name(user.settings[2])
	l4 = "Slide: %s" % pygame.key.name(user.settings[3])
	l5 = "Super Jumping: %s + %s" % (pygame.key.name(user.settings[3]), pygame.key.name(user.settings[2]))
	surf_text = fonts[2].render(l1, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 225))
	surf_text = fonts[2].render(l2, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 325))
	surf_text = fonts[2].render(l3, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 425))
	surf_text = fonts[2].render(l4, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 525))
	surf_text = fonts[2].render(l5, True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 625))

	for button in buttons:
		button.draw(win)

def draw_settings(win: pygame.Surface, fonts: pygame.font, player: Player, buttons, input_rects, user_texts, input_colors, texts):
	win.fill("#6fcae8")
	surf_text = fonts[0].render("SETTINGS", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 100))
	surf_text = fonts[1].render("press enter to confirm key change", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 900))
	surf_text = fonts[1].render("not all keys allowed as inputs", True, "#ffffff")
	win.blit(surf_text, ((win.get_width() - surf_text.get_width())/2, 1000))
	for i in range(len(input_rects)):
		user_text = user_texts[i]
		color = input_colors[i]
		input_rect = input_rects[i]
		text_surface = fonts[2].render(user_text, True, "#ffffff")
		input_rect.draw(win)
		win.blit(text_surface, (input_rect._pt._x + (input_rect._w / 2) - (text_surface.get_width() / 2), input_rect._pt._y + (input_rect._h / 2) - (text_surface.get_height() / 2)))
		win.blit(texts[i], ((win.get_width() / 2) - (texts[1].get_width() / 2) - (texts[i].get_width() / 2) - 10, input_rect._pt._y + (input_rect._h / 2) - (texts[i].get_height() / 2)))
	for button in buttons:
		button.draw(win)

def save_map(walls: list[Surface], f_name) -> None:
	f = open(f_name, "w")
	for wall in walls:
		if wall.get_is_teleport():
			pos = "{},{},{},{},{},{},{}\n"
			f.write(pos.format(int(wall.get_is_teleport()), wall.get_pt().get_x(), wall.get_pt().get_y(), wall.get_w(), wall.get_h(), float(wall.get_friction()), wall.get_num()))
		else:
			pos = "{},{},{},{},{},{},{},{}\n"
			f.write(pos.format(int(wall.get_is_teleport()), wall.get_pt().get_x(), wall.get_pt().get_y(), wall.get_w(), wall.get_h(), float(wall.get_friction()), int(wall.get_can_kill()), int(wall.get_is_finish())))
	f.close()

def save_times(times, map) -> None:
	if map == "0":
		f = open("map_data/map_1/times.txt", 'w')
	elif map == "1":
		f = open("map_data/ch1/times.txt", 'w')
	elif map == "2":
		f = open("map_data/ch2/times.txt", 'w')
	elif map == "3":
		f = open("map_data/ch3/times.txt", 'w')
	elif map == "4":
		f = open("map_data/ch4/times.txt", 'w')
	elif map == "5":
		f = open("map_data/ch5/times.txt", 'w')
	elif map == "6":
		f = open("map_data/ch6/times.txt", 'w')
	elif map == "7":
		f = open("map_data/ch7/times.txt", 'w')
	elif map == "8":
		f = open("map_data/map_2/times.txt", 'w')
	else:
		f = []
	if f != []:
		for time in times:
			f.write(str(time) + "\n")
		f.close()

def load_times(map) -> None:
	times = []
	if map == "0":
		f = open("map_data/map_1/times.txt", 'r')
	elif map == "1":
		f = open("map_data/ch1/times.txt", 'r')
	elif map == "2":
		f = open("map_data/ch2/times.txt", 'r')
	elif map == "3":
		f = open("map_data/ch3/times.txt", 'r')
	elif map == "4":
		f = open("map_data/ch4/times.txt", 'r')
	elif map == "5":
		f = open("map_data/ch5/times.txt", 'r')
	elif map == "6":
		f = open("map_data/ch6/times.txt", 'r')
	elif map == "7":
		f = open("map_data/ch7/times.txt", 'r')
	elif map == "8":
		f = open("map_data/map_2/times.txt", 'r')
	else:
		f = []

	if f != []:
		for line in f:
			line = line.strip()
			times.append(line)
		f.close()
	return times

def load_map(map: int) -> list[Surface]:
	walls = []
	getting_times = False
	if str(map) == "0":
		f = open("map_data/map_1/walls.txt", 'r')
	elif str(map) == "1":
		f = open("map_data/ch1/walls.txt", 'r')
	elif str(map) == "2":
		f = open("map_data/ch2/walls.txt", 'r')
	elif str(map) == "3":
		f = open("map_data/ch3/walls.txt", 'r')
	elif str(map) == "4":
		f = open("map_data/ch4/walls.txt", 'r')
	elif str(map) == "5":
		f = open("map_data/ch5/walls.txt", 'r')
	elif str(map) == "6":
		f = open("map_data/ch6/walls.txt", 'r')
	elif str(map) == "7":
		f = open("map_data/ch7/walls.txt", 'r')
	elif str(map) == "8":
		f = open("map_data/map_2/walls.txt", 'r')
	else:
		f = []

	for line in f:
		line = line.strip()
		stats = line.split(",")
		# print(stats[5], stats[6])
		# print(stats[5] == 1)
		if int(stats[0]) == 1:
			# print(stats[6])
			wall = Teleporter(Vector(int(stats[1]), int(stats[2])), int(stats[3]), int(stats[4]), None, int(stats[6]), float(stats[5]))
			# print(wall.get_num())
		else:
			if float(stats[5]) == 0:
				color = "#8df6ec"
				kill = False
				end = False
			elif float(stats[5]) > 0:
				color = "#22ab7d"
				kill = False
				end = False
			elif int(stats[6]) == 1:
				# print("aaaaaa")
				color = "#ff0000"
				kill = True
				end = False
			elif int(stats[7]) == 1:
				# print("bbbbbb")
				color = "#999900"
				kill = False
				end = True
			else:
				# print("ccccc")
				color = "#000000"
				kill = False
				end = False
			wall = Surface(Vector(int(stats[1]), int(stats[2])), int(stats[3]), int(stats[4]), float(stats[5]), color, kill, end, False)
		# print(wall.get_can_kill(), wall.get_is_finish())
		walls.append(wall)
	if f != []:
		f.close()
	teleporters = []
	for wall in walls:
		if wall.get_is_teleport():
			wall.set_next_tp(wall)
			teleporters.append(wall)
	# print(teleporters)
	return walls, teleporters

def save_user(user):
	f = open("userSettings.txt", 'w')
	for setting in user.settings:
		f.write(str(setting) + "\n")
	f.close()

def load_user():
	user = User()
	f = open("userSettings.txt", 'r')
	index = 0
	for line in f:
		line = line.strip()
		if index < 4:
			user.set_setting(index, int(line))
			index += 1
		elif index == 4:
			# print(str(line), str(line) == "True")
			if str(line) == "True":
				# print("yes")
				user.set_setting(index, True)
			else:
				# print("no")
				user.set_setting(index, False)
			# print(user.settings, user.music_on)

	f.close()
	# print(user.settings, user.music_on)
	return user

def create_buttons(win: pygame.Surface, font: pygame.font, user):
	# 40 font
	surf_text = font.render("PLAY", True, "#000000")
	play_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.35), surf_text.get_width(), surf_text.get_height(), "PLAY", False, "selection", font)
	surf_text = font.render("LEADERBOARDS", True, "#000000")
	leaderboard_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.5), surf_text.get_width(), surf_text.get_height(), "LEADERBOARDS", False, "selc_leaderboard", font)
	surf_text = font.render("SETTINGS", True, "#000000")
	settings_button_1 = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.8), surf_text.get_width(), surf_text.get_height(), "SETTINGS", False, "settings", font)
	surf_text = font.render("CONTROLS", True, "#000000")
	mechanics_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.65), surf_text.get_width(), surf_text.get_height(), "CONTROLS", False, "mechanics", font)
	surf_text = font.render("PLAY AGAIN", True, "#000000")
	dead_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, 500), surf_text.get_width(), surf_text.get_height(), "PLAY AGAIN", False, "respawn", font, "#ffffff")
	f_play_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * .35), surf_text.get_width(), surf_text.get_height(), "PLAY AGAIN", False, "respawn", font)
	surf_text = font.render("BACK TO MAIN MENU", True, "#000000")
	menu_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, win.get_height() * 0.6), surf_text.get_width(), surf_text.get_height(), "BACK TO MAIN MENU", False, "welcome", font)
	d_menu_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, 800), surf_text.get_width(), surf_text.get_height(), "BACK TO MAIN MENU", False, "welcome", font, "#ffffff")
	surf_text = font.render("RESUME GAME", True, "#000000")
	return_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, 300), surf_text.get_width(), surf_text.get_height(), "RESUME GAME", False, "game", font, "#ffffff")
	surf_text = font.render("MAIN MENU", True, "#000000")
	p_menu_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, 700), surf_text.get_width(), surf_text.get_height(), "MAIN MENU", False, "welcome", font, "#ffffff")
	surf_text = font.render("SETTINGS", True, "#000000")
	settings_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, 433.33), surf_text.get_width(), surf_text.get_height(), "SETTINGS", False, "settings_game", font, "#ffffff")
	surf_text = font.render("RESTART", True, "#000000")
	restart_button = Button(Vector(win.get_width() / 2 - surf_text.get_width()/2, 566.66), surf_text.get_width(), surf_text.get_height(), "RESTART", False, "restart", font, "#ffffff")
	surf_text = font.render("BACK", True, "#000000")
	back_button = Button(Vector(win.get_width() / 20, win.get_height() * 0.05), surf_text.get_width(), surf_text.get_height(), "BACK", False, "welcome", font)
	surf_text = font.render("PLAY TRAINING COURSE", True, "#000000")
	s_train_button = Button(Vector(win.get_width() / 20, 600), surf_text.get_width(), surf_text.get_height(), "PLAY TRAINING COURSE", False, "0", font, "#f09e24")
	surf_text = font.render("PLAY ICE PEAK", True, "#000000")
	s_ice_button = Button(Vector(win.get_width() / 20, s_train_button.get_pt().get_y() + s_train_button.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY ICE PEAK", False, "8", font, "#f03524")
	surf_text = font.render("PLAY CHALLENGES", True, "#000000")
	s_tut_button = Button(Vector(win.get_width() / 20, s_train_button.get_pt().get_y() - 20 - surf_text.get_height()), surf_text.get_width(), surf_text.get_height(), "PLAY CHALLENGES", False, "challenge", font)
	surf_text = font.render("BACK", True, "#000000")
	t_back_button = Button(Vector(win.get_width() / 20, win.get_height() * 0.05), surf_text.get_width(), surf_text.get_height(), "BACK", False, "selection", font)
	surf_text = font.render("PLAY JUMPING CHALLENGE", True, "#000000")
	t_1 = Button(Vector(win.get_width() / 20, 400), surf_text.get_width(), surf_text.get_height(), "PLAY JUMPING CHALLENGE", False, "1", font, "#127802")
	surf_text = font.render("PLAY DOUBLE JUMPING CHALLENGE", True, "#000000")
	t_2 = Button(Vector(win.get_width() / 20, t_1.get_pt().get_y() + t_1.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY DOUBLE JUMPING CHALLENGE", False, "2", font, "#127802")
	surf_text = font.render("PLAY SLIDING CHALLENGE", True, "#000000")
	t_3 = Button(Vector(win.get_width() / 20, t_2.get_pt().get_y() + t_2.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY SLIDING CHALLENGE", False, "3", font, "#127802")
	surf_text = font.render("PLAY SLIDING JUMPING CHALLENGE", True, "#000000")
	t_4 = Button(Vector(win.get_width() / 20, t_3.get_pt().get_y() + t_3.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY SLIDING JUMPING CHALLENGE", False, "4", font, "#127802")
	surf_text = font.render("PLAY WALL BOUNCE CHALLENGE", True, "#000000")
	t_5 = Button(Vector(win.get_width() / 20, t_4.get_pt().get_y() + t_4.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY WALL BOUNCE CHALLENGE", False, "5", font, "#127802")
	surf_text = font.render("PLAY DEATH CHALLENGE", True, "#000000")
	t_6 = Button(Vector(win.get_width() / 20, t_5.get_pt().get_y() + t_5.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY DEATH CHALLENGE", False, "6", font, "#127802")
	surf_text = font.render("PLAY ULTIMATE CHALLENGE", True, "#000000")
	t_7 = Button(Vector(win.get_width() / 20, t_6.get_pt().get_y() + t_6.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "PLAY ULTIMATE CHALLENGE", False, "7", font, "#f09e24")
	surf_text = font.render("NEXT LEVEL", True, "#000000")
	continue_button = Button(Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * .475), surf_text.get_width(), surf_text.get_height(), "NEXT LEVEL", False, "continue", font)
	surf_text = font.render("EXIT TO DESKTOP", True, "#000000")
	p_exit_button = Button(Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * .8), surf_text.get_width(), surf_text.get_height(), "EXIT TO DESKTOP", False, "exit", font)
	exit_button = Button(Vector(win.get_width() - surf_text.get_width(), win.get_height() - surf_text.get_height()), surf_text.get_width(), surf_text.get_height(), "EXIT TO DESKTOP", False, "exit", font)

	surf_text = font.render("JUMPING CHALLENGE", True, "#000000")
	l_1 = Button(Vector(win.get_width() / 20, 400), surf_text.get_width(), surf_text.get_height(), "JUMPING CHALLENGE", False, "1", font)
	surf_text = font.render("DOUBLE JUMPING CHALLENGE", True, "#000000")
	l_2 = Button(Vector(win.get_width() / 20, l_1.get_pt().get_y() + l_1.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "DOUBLE JUMPING CHALLENGE", False, "2", font)
	surf_text = font.render("SLIDING CHALLENGE", True, "#000000")
	l_3 = Button(Vector(win.get_width() / 20, l_2.get_pt().get_y() + l_2.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "SLIDING CHALLENGE", False, "3", font)
	surf_text = font.render("SLIDING JUMPING CHALLENGE", True, "#000000")
	l_4 = Button(Vector(win.get_width() / 20, l_3.get_pt().get_y() + l_3.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "SLIDING JUMPING CHALLENGE", False, "4", font)
	surf_text = font.render("WALL BOUNCE CHALLENGE", True, "#000000")
	l_5 = Button(Vector(win.get_width() / 20, l_4.get_pt().get_y() + l_4.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "WALL BOUNCE CHALLENGE", False, "5", font)
	surf_text = font.render("DEATH CHALLENGE", True, "#000000")
	l_6 = Button(Vector(win.get_width() / 20, l_5.get_pt().get_y() + l_5.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "DEATH CHALLENGE", False, "6", font)
	surf_text = font.render("ULTIMATE CHALLENGE", True, "#000000")
	l_7 = Button(Vector(win.get_width() / 20, l_6.get_pt().get_y() + l_6.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "ULTIMATE CHALLENGE", False, "7", font)
	surf_text = font.render("TRAINING COURSE", True, "#000000")
	l_0 = Button(Vector(win.get_width() / 2, 400), surf_text.get_width(), surf_text.get_height(), "TRAINING COURSE", False, "0", font)
	surf_text = font.render("ICE PEAK", True, "#000000")
	l_8 = Button(Vector(win.get_width() / 2, l_0.get_pt().get_y() + l_0.get_h() + 20), surf_text.get_width(), surf_text.get_height(), "ICE PEAK", False, "8", font)

	surf_text = font.render("BACK", True, "#000000")
	l_back_button = Button(Vector(win.get_width() / 20, win.get_height() * 0.05), surf_text.get_width(), surf_text.get_height(), "BACK", False, "selc_leaderboard", font)
	surf_text = font.render("BACK", True, "#000000")
	selc_l_back_button = Button(Vector(win.get_width() / 20, win.get_height() * 0.05), surf_text.get_width(), surf_text.get_height(), "BACK", False, "welcome", font)

	surf_text = font.render("MUSIC ON/OFF", True, "#000000")
	if user.music_on:
		color = "#12d932"
	else:
		color = "#ff0000"
	music_button = ToggleButton(Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * .7), surf_text.get_width(), surf_text.get_height(), "MUSIC ON/OFF", user, user.music_on, False, "settings", font, color)

	surf_text = font.render("BACK", True, "#000000")
	back_game_button = Button(Vector(win.get_width() / 20, win.get_height() * 0.05), surf_text.get_width(), surf_text.get_height(), "BACK", False, "pause", font)

	welc_buttons = [play_button, leaderboard_button, exit_button, mechanics_button, settings_button_1]
	selc_buttons = [back_button, s_train_button, s_ice_button, s_tut_button, exit_button]
	challenge_buttons = [t_back_button, t_1, t_2, t_3, t_4, t_5, t_6, t_7, exit_button]
	challenge_fin_buttons = [f_play_button, menu_button, continue_button, p_exit_button]
	fin_buttons = [f_play_button, menu_button, p_exit_button]
	dead_buttons = [dead_button, d_menu_button, p_exit_button]
	pause_buttons = [return_button, p_menu_button, settings_button, p_exit_button, restart_button]
	selc_leaderboard_buttons = [selc_l_back_button, l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_0, l_8, exit_button]
	leaderboard_buttons = [l_back_button, exit_button]
	controls_buttons = [back_button, exit_button]
	settings_buttons = [back_button, exit_button, music_button]
	settings_game_buttons = [back_game_button, exit_button, music_button]
	buttons = []

	return buttons, welc_buttons, selc_buttons, challenge_buttons, challenge_fin_buttons, fin_buttons, dead_buttons, pause_buttons, selc_leaderboard_buttons, leaderboard_buttons, controls_buttons, settings_buttons, settings_game_buttons

def load_level(level: int) -> list[Surface]:
	if level == 0:
		walls = [
			# Surface(Vector(,), , , ),
			Surface(Vector(0, 800), 1920, 580, -.15),
			Surface(Vector(0, -25000), 10, 51100, -.1),
			Surface(Vector(1910, -25000), 10, 51100, -.1),
			Surface(Vector(0, -25100), 1920, 1000, -.1),
			# End of base walls (no teleporters on this map), it is relatively blocked out, no death
		]
		teleporters = []
		for wall in walls:
			if wall.get_is_teleport():
				wall.set_next_tp(wall)
				teleporters.append(wall)
		return walls, teleporters
	else:
		return [], []

def main():
	# maps = ["map_data/ch1/walls.txt", "map_data/ch2/walls.txt", "map_data/ch3/walls.txt", "map_data/ch4/walls.txt", "map_data/ch5/walls.txt", "map_data/ch6/walls.txt", "map_data/ch7/walls.txt", "map_data/map_1/walls.txt", "map_data/map_2/walls.txt"]
	# for i in range(len(maps)):
	delta = 0.017 # second since last frame
	last_frame = time.time()

	screen = "welcome"
	previous_screen = "welcome"
	game_status = True

	# clock = pygame.time.Clock()
	start_time = datetime.datetime.now()

	win = create_window()
	fonts = create_fonts()

	# print(K_LCTRL)

	# print(pygame.font.get_fonts())
	user = load_user()
	# user = User()
	# save_user(user)
	player = Player(user)
	# walls = load_map(0)
	walls = []
	teleporters = []
	times = []
	hb_mouse = Hitbox(Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5), 10, 10, "#ff00ff")
	buttons, welc_buttons, selc_buttons, challenge_buttons, challenge_fin_buttons, fin_buttons, dead_buttons, pause_buttons, selc_leaderboard_buttons, leaderboard_buttons, control_buttons, settings_buttons, settings_game_buttons = create_buttons(win, fonts[2], user)
	current_map = 0
	was_down = False
	map_name = ""
	in_challenge = False
	elapsed_time = start_time
	deaths = [0]

	escape_down = DownPress()

	# Text input stuff
	user_texts = ['', '', '', '']
	for i in range(len(user_texts)):
		if i < 4:
			user_texts[i] = pygame.key.name(int(user.settings[i]))
	input_rects = [Hitbox(Vector(win.get_width() / 2 + 10, 200), 300, 100, "#464553"), Hitbox(Vector(win.get_width() / 2 + 10, 350), 300, 100, "#464553"), Hitbox(Vector(win.get_width() / 2 + 10, 500), 300, 100, "#464553"), Hitbox(Vector(win.get_width() / 2 + 10, 650), 300, 100, "#464553")]
	actives = [False, False, False, False]
	color_active = "#a9a9ac"
	color_passive = "#464553"
	input_colors = [color_passive, color_passive, color_passive, color_passive]

	setting_texts = [fonts[2].render("WALK LEFT", True, "#ffffff"), fonts[2].render("WALK RIGHT", True, "#ffffff"), fonts[2].render("JUMP", True, "#ffffff"), fonts[2].render("SLIDE", True, "#ffffff")]
	extra_keys = [K_LALT, K_LALT, K_LCTRL, K_RCTRL, K_LSHIFT, K_RSHIFT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SCROLLOCK, K_CAPSLOCK, K_NUMLOCK, K_F15, K_F14, K_F13, K_F12, K_F11, K_F10, K_F9, K_F8, K_F7, K_F6, K_F5, K_F4, K_F3, K_F2, K_F1,]

	while game_status:
		delta = time.time() - last_frame
		last_frame = time.time()
		handle_events(user)
		# print(tes)
		keys = pygame.key.get_pressed()
		# print(keys, "aaaaaaaaaaaaaaa")
		# for i in range(len(keys)):
		# 	# print(keys_down[i])
		# 	if keys[i] == 1:
		# 		print(i, "AAAAAAAAAAA")
		screen = handle_keys(screen, player, hb_mouse, delta, walls, teleporters, elapsed_time, times, current_map, deaths, keys, escape_down)
		mouse_buttons_down = pygame.mouse.get_pressed()
		# print(screen)
		if screen == "welcome":
			screen, was_down = handle_mouse(screen, hb_mouse, welc_buttons, was_down, mouse_buttons_down)
		elif screen == "selection":
			screen, was_down = handle_mouse(screen, hb_mouse, selc_buttons, was_down, mouse_buttons_down)
		elif screen == "challenge":
			screen, was_down = handle_mouse(screen, hb_mouse, challenge_buttons, was_down, mouse_buttons_down)
			# print(screen)
		elif screen == "finished":
			if in_challenge and current_map != 7:
				f_buttons = challenge_fin_buttons
			else:
				f_buttons = fin_buttons
			screen, was_down = handle_mouse(screen, hb_mouse, f_buttons, was_down, mouse_buttons_down)
		elif screen == "dead":
			screen, was_down = handle_mouse(screen, hb_mouse, dead_buttons, was_down, mouse_buttons_down)
		elif screen == "pause":
			screen, was_down = handle_mouse(screen, hb_mouse, pause_buttons, was_down, mouse_buttons_down)
		elif screen == "settings":
			handle_inputs(win, fonts[2], input_rects, actives, user_texts, input_colors, color_passive, color_active, user, hb_mouse, was_down, keys, mouse_buttons_down, extra_keys)
			screen, was_down = handle_mouse(screen, hb_mouse, settings_buttons, was_down, mouse_buttons_down)
		elif screen == "settings_game":
			handle_inputs(win, fonts[2], input_rects, actives, user_texts, input_colors, color_passive, color_active, user, hb_mouse, was_down, keys, mouse_buttons_down, extra_keys)
			screen, was_down = handle_mouse(screen, hb_mouse, settings_game_buttons, was_down, mouse_buttons_down)
		elif screen == "selc_leaderboard":
			screen, was_down = handle_mouse(screen, hb_mouse, selc_leaderboard_buttons, was_down, mouse_buttons_down)
		elif screen == "leaderboard":
			screen, was_down = handle_mouse(screen, hb_mouse, leaderboard_buttons, was_down, mouse_buttons_down)
		elif screen == "mechanics":
			screen, was_down = handle_mouse(screen, hb_mouse, control_buttons, was_down, mouse_buttons_down)
		else:
			screen, was_down = handle_mouse(screen, hb_mouse, buttons, was_down, mouse_buttons_down)

		if len(screen.split(":")) > 1:
			screen = screen.split(":")
			current_map = str(screen[1])
			screen = "leaderboard"
			times = load_times(current_map)
			# print(current_map + " aaaaaaaaaaaaaa")
			if current_map == "0":
				map_name = "Training Course"
			elif current_map == "1":
				map_name = "Jumping Challenge"
			elif current_map == "2":
				map_name = "Double Jumping Challenge"
			elif current_map == "3":
				map_name = "Sliding Challenge"
			elif current_map == "4":
				map_name = "Slide Jumping Challenge"
			elif current_map == "5":
				map_name = "Wall Bounce Challenge"
			elif current_map == "6":
				map_name = "Death Challenge"
			elif current_map == "7":
				map_name = "Ultimate Challenge"
			elif current_map == "8":
				map_name = "ICE PEAK"
			else:
				screen = "selc_leaderboard"
		else:
			if "0" <= screen <= "8":
				start_time = datetime.datetime.now()
				current_map = int(screen)
				walls, teleporters = load_map(current_map)
				times = load_times(str(current_map))
				player = Player(user)
				screen = "game"
				if 1 <= current_map <= 7:
					in_challenge = True
				else:
					in_challenge = False
				deaths[0] = 0
			elif screen == "continue":
				start_time = datetime.datetime.now()
				current_map += 1
				walls, teleporters = load_map(current_map)
				times = load_times(str(current_map))
				player = Player(user)
				screen = "game"
				in_challenge = True
				deaths[0] = 0

		if screen == "respawn" or screen == "restart":
			if player.get_is_finished() or screen == "restart":
				start_time = datetime.datetime.now()
				deaths[0] = 0
				player = Player(user)
				active_tps = []
			else:
				player = Player(user)
				active_tps = []
				if teleporters != []:
					next_tp = teleporters[0].get_next_tp()
					for tp in teleporters:
						if tp.get_is_active():
							active_tps.append(tp.get_num())

			walls, teleporters = load_map(current_map)
			for i in active_tps:
				teleporters[i].set_is_active(True)
				# print(next_tp)
				# if teleporters[i] == next_tp:
				# 	print("same")
				teleporters[i].set_next_tp(teleporters[active_tps[len(active_tps) - 1]])
			screen = "game"

		if screen == "game":
			elapsed_time = datetime.datetime.now() - start_time
			# print(datetime.datetime.now())
			# print(win)
			draw_game(win, fonts[1], player, walls, hb_mouse, delta, elapsed_time)
			# print(elapsed_time)
		elif screen == "welcome":
			draw_welcome(win, fonts[0], hb_mouse, welc_buttons)
		elif screen == "selection":
			draw_selection(win, fonts[0], hb_mouse, selc_buttons)
		elif screen == "challenge":
			draw_challenge(win, fonts[0], hb_mouse, challenge_buttons)
		elif screen == "dead":
			start_time = datetime.datetime.now() - elapsed_time
			draw_dead(win, fonts[0], player, walls, hb_mouse, delta, dead_buttons, deaths)
		elif screen == "pause":
			start_time = datetime.datetime.now() - elapsed_time
			draw_pause(win, fonts[0], player, walls, hb_mouse, delta, pause_buttons)
		elif screen == "settings":
			draw_settings(win, fonts, player, settings_buttons, input_rects, user_texts, input_colors, setting_texts)
		elif screen == "settings_game":
			draw_settings(win, fonts, player, settings_game_buttons, input_rects, user_texts, input_colors, setting_texts)
		elif screen == "finished":
			if in_challenge and current_map != 7:
				f_buttons = challenge_fin_buttons
			else:
				f_buttons = fin_buttons
			draw_finished(win, fonts[0], player, walls, hb_mouse, delta, f_buttons, elapsed_time)
		elif screen == "leaderboard":
			draw_leaderboard(win, fonts, times, map_name, leaderboard_buttons)
		elif screen == "selc_leaderboard":
			draw_selc_leaderboard(win, fonts[0], selc_leaderboard_buttons)
		elif screen == "mechanics":
			draw_mechanics(win, fonts, control_buttons, user)
		if screen == "exit":
			save_user(user)
			pygame.quit()
			sys.exit()
			quit()
		pygame.display.flip()
		# print(user.settings)

		# clock.tick_busy_loop(200)

		# print("Delta: %1.3f\tFPS: %4.2f" % (delta, 1/delta))


main()
