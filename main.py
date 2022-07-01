from __future__ import annotations  # for type hints
import pygame  # graphics library
from pygame.locals import *  # for keyboard input (ex: 'K_w')
import time  # for fps/delta
import datetime  # for timer

from classes import (
    Vector,
    Hitbox,
    HitboxPart,
    AdvancedHitbox,
    Player,
    Surface,
    Teleporter,
    Button,
    Map,
)


def calc_average(lst: list[float]) -> float:
    if len(lst) == 0:
        return 1 / 100
    return sum(lst) / len(lst)


def create_window() -> pygame.Surface:
    pygame.init()
    win = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("TempName: v-0.94")
    return win
    # s.set_alpha(128)                # alpha level
    # s.fill((255,255,255))           # this fills the entire surface
    # windowSurface.blit(s, (0,0))    # (0,0) are the top-left coordinates


def create_fonts() -> list[pygame.Font]:
    fonts = []
    font_1 = pygame.font.SysFont("Monospace", 60)
    font_1.set_bold(True)
    font_2 = pygame.font.SysFont("Monospace", 30)
    font_2.set_bold(True)
    font_3 = pygame.font.SysFont("Monospace", 40)
    font_3.set_bold(True)
    fonts.append(font_1)
    fonts.append(font_2)
    fonts.append(font_3)

    return fonts


def handle_events() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def handle_keys(
    screen: str,
    player: Player,
    hb_mouse,
    delta: float,
    walls,
    teleporters,
    elapsed_time,
    times: list[datetime.datetime],
) -> str:
    keys_down = pygame.key.get_pressed()
    if (keys_down[K_RCTRL] or keys_down[K_LCTRL]) and keys_down[K_q]:
        pygame.quit()
        quit()
    # elif screen == "welcome" and keys_down[K_RETURN]:
    # 	return "game"
    elif keys_down[K_ESCAPE] and (screen == "game" or screen == "dead"):
        return "pause"
    elif screen == "game" and not player.is_alive:
        return "dead"
    elif screen == "game":
        player.handle_keys(keys_down, hb_mouse, delta, walls, teleporters)
        if player.is_finished:
            if elapsed_time < times[0]:
                times.insert(0, elapsed_time)
            return "finished"
    elif screen == "dead" and keys_down[K_RETURN]:
        return "game"
    return screen


def handle_mouse(
    screen: str, hb_mouse: Hitbox, buttons: list[Button], was_down: bool
) -> str:
    hb_mouse.pt = Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5)
    mouse_buttons_down = pygame.mouse.get_pressed()
    if mouse_buttons_down[0]:
        # hb_mouse.set_color("#ff0000")
        for button in buttons:
            if hb_mouse.check_collide(button) and not was_down:
                was_down = True
                return button.next_loc, was_down
    else:
        was_down = False
    # 	hb_mouse.set_color("#ff00ff")
    return screen, was_down


def draw_welcome(
    win: pygame.Surface, font: pygame.font, hb_mouse: Hitbox, buttons: list[Button]
) -> None:
    # 60 font
    win.fill("#fdf6e3")
    surf_text = font.render("WHAT GOES UP...", True, "#ff0000")
    win.blit(surf_text, ((win.get_width() - surf_text.get_width()) / 2, 100))
    for button in buttons:
        button.draw(win)
    # hb_mouse.draw(win)


def draw_selection(
    win: pygame.Surface, font: pygame.font, hb_mouse: Hitbox, buttons: list[Button]
) -> None:
    # 60 font
    win.fill("#fdf6e3")
    surf_text = font.render("MAP SELECTION", True, "#000000")
    win.blit(surf_text, ((win.get_width() - surf_text.get_width()) / 2, 200))

    for button in buttons:
        button.draw(win)
    # hb_mouse.draw(win)


def draw_challenge(
    win: pygame.Surface,
    font: pygame.font,
    hb_mouse: Hitbox,
    buttons: list[Button],
    # times,
) -> None:
    win.fill("#fdf6e3")
    surf_text = font.render("challenge", True, "#000000")
    win.blit(surf_text, ((win.get_width() - surf_text.get_width()) / 2, 200))

    for button in buttons:
        button.draw(win)
        # if
        surf_text = font.render("")


def draw_game(
    win: pygame.Surface,
    font: pygame.font,
    player: Player,
    walls: list[Surface],
    hb_mouse: Hitbox,
    delta: float,
    elapsed_time,
) -> None:
    # 30 font
    win.fill("#fdf6e3")
    # use pygame.Surface.scroll for when background is an image
    for wall in walls:
        wall.draw(win)
    player.draw(win)

    # Elapsed time
    t = str(elapsed_time).split(".")
    surf_time_text = font.render("Time: " + str(t[0]), True, "#ffffff")
    fps = 1 / delta
    surf_fps_text = font.render("FPS: %4.0f" % fps, True, "#ffffff")
    height = surf_time_text.get_height() + surf_fps_text.get_height() + 30
    font_rect = (0, 0, surf_time_text.get_width() + win.get_width() * 0.075, height)
    pygame.draw.rect(win, "#000000", font_rect)
    win.blit(surf_time_text, ((win.get_width() * 0.0375, 10)))
    win.blit(surf_fps_text, ((win.get_width() * 0.0375, 40)))

    # hb_mouse.draw(win)


def draw_dead(
    win: pygame.Surface,
    font: pygame.font,
    player: Player,
    walls: list[Surface],
    hb_mouse: Hitbox,
    delta: float,
    buttons: list[Button],
) -> None:
    # 60 font
    win.fill("#fdf6e3")
    # use pygame.Surface.scroll for when background is an image
    for wall in walls:
        wall.draw(win)
    player.draw(win)

    # hb_mouse.draw(win)
    # Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
    rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
    rect.fill((0, 0, 0, 128))  # this fills the entire surface
    win.blit(rect, (0, 0))  # (0,0) are the top-left coordinates
    surf_text = font.render("YOU HAVE DIED", True, "#ffffff")
    win.blit(surf_text, ((win.get_width() - surf_text.get_width()) / 2, 100))
    for button in buttons:
        button.draw(win)
    # hb_mouse.draw(win)


def draw_pause(
    win: pygame.Surface,
    font: pygame.font,
    player: Player,
    walls: list[Surface],
    hb_mouse: Hitbox,
    delta: float,
    buttons: list[Button],
) -> None:
    # 60 font
    win.fill("#fdf6e3")
    # use pygame.Surface.scroll for when background is an image
    for wall in walls:
        wall.draw(win)
    player.draw(win)

    # hb_mouse.draw(win)
    # Work on making it opaque when player dies. Or just add a different screen. The rest of the code works though?
    rect = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
    rect.fill((0, 0, 0, 128))  # this fills the entire surface
    win.blit(rect, (0, 0))  # (0,0) are the top-left coordinates
    surf_text = font.render("OPTIONS", True, "#ffffff")
    win.blit(surf_text, ((win.get_width() - surf_text.get_width()) / 2, 100))
    for button in buttons:
        button.draw(win)
    # hb_mouse.draw(win)


def draw_finished(
    win: pygame.Surface,
    font: pygame.font,
    player: Player,
    walls: list[Surface],
    hb_mouse: Hitbox,
    delta: float,
    buttons: list[Button],
) -> None:
    # 60 font
    # win.fill("#3973fa")
    win.fill("#fdf6e3")
    surf_text = font.render("YOU FINISHED", True, "#ff0000")
    win.blit(surf_text, ((win.get_width() - surf_text.get_width()) / 2, 100))
    for button in buttons:
        button.draw(win)
    # hb_mouse.draw(win)


def save_map(walls: list[Surface]) -> None:
    f_name = input("File Name: ")
    f = open(f_name, "w")
    for wall in walls:
        if wall.is_teleport:
            pos = "{},{},{},{},{},{},{}\n"
            f.write(
                pos.format(
                    int(wall.is_teleport),
                    wall.pt.x,
                    wall.pt.y,
                    wall.w,
                    wall.h,
                    float(wall.friction),
                    wall.num,
                )
            )
        else:
            pos = "{},{},{},{},{},{},{},{}\n"
            f.write(
                pos.format(
                    int(wall.is_teleport),
                    wall.pt.x,
                    wall.pt.y,
                    wall.w,
                    wall.h,
                    float(wall.friction),
                    int(wall.can_kill),
                    int(wall.is_finish),
                )
            )
    f.close()


def load_map(map_num: int) -> list[Surface]:
    walls = []
    if map_num == 0:
        f = open("map_data/map_1.txt", "r")
        for line in f:
            line = line.strip()
            stats = line.split(",")
            if int(stats[0]) == 1:
                wall = Teleporter(
                    Vector(int(stats[1]), int(stats[2])),
                    int(stats[3]),
                    int(stats[4]),
                    None,
                    int(stats[6]),
                    float(stats[5]),
                )
            else:
                if float(stats[5]) > 0:
                    color = "#22ab7d"
                elif int(stats[6]) == 1:
                    color = "#ff0000"
                    kill = True
                elif int(stats[7]) == 1:
                    color = "#999900"
                    end = True
                else:
                    color = "#000000"
                    kill = False
                    end = False
                wall = Surface(
                    Vector(int(stats[1]), int(stats[2])),
                    int(stats[3]),
                    int(stats[4]),
                    float(stats[5]),
                    color,
                    kill,
                    end,
                    False,
                )
            walls.append(wall)
        f.close()
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
    return walls, teleporters


def load_map_data() -> list:
    f = open("map_data/all_map_data.txt", "r")
    maps = []
    map_data = []
    for line in f:
        line = line.strip()
        if line == "break":
            map = Map(map_data[0], map_data[1], map_data[2], map_data[3])
            maps.append(map)
            map_data = []
        elif line == "end":
            break
        else:
            stats = line.split("=")
            map_data.append(stats[1])
    f.close()
    return maps


def create_buttons(
    win: pygame.Surface,
    font: pygame.font,
):
    # 40 font
    surf_text = font.render("PLAY", True, "#000000")
    play_button = Button(
        Vector(
            win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.35
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY",
        False,
        "selection",
        font,
    )
    surf_text = font.render("PLAY AGAIN", True, "#000000")
    dead_button = Button(
        Vector(
            win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.35
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY AGAIN",
        False,
        "respawn",
        font,
        "#ffffff",
    )
    f_play_button = Button(
        Vector(
            win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.35
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY AGAIN",
        False,
        "respawn",
        font,
    )
    surf_text = font.render("BACK TO MAIN MENU", True, "#000000")
    menu_button = Button(
        Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.6),
        surf_text.get_width(),
        surf_text.get_height(),
        "BACK TO MAIN MENU",
        False,
        "welcome",
        font,
    )
    d_menu_button = Button(
        Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.6),
        surf_text.get_width(),
        surf_text.get_height(),
        "BACK TO MAIN MENU",
        False,
        "welcome",
        font,
        "#ffffff",
    )
    surf_text = font.render("RESUME GAME", True, "#000000")
    return_button = Button(
        Vector(
            win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.35
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "RESUME GAME",
        False,
        "game",
        font,
        "#ffffff",
    )
    surf_text = font.render("MAIN MENU", True, "#000000")
    p_menu_button = Button(
        Vector(
            win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.65
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "MAIN MENU",
        False,
        "welcome",
        font,
        "#ffffff",
    )
    surf_text = font.render("SETTINGS", True, "#000000")
    settings_button = Button(
        Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.5),
        surf_text.get_width(),
        surf_text.get_height(),
        "SETTINGS",
        False,
        "settings",
        font,
        "#ffffff",
    )
    surf_text = font.render("BACK", True, "#000000")
    back_button = Button(
        Vector(win.get_width() / 20, win.get_height() * 0.05),
        surf_text.get_width(),
        surf_text.get_height(),
        "BACK",
        False,
        "welcome",
        font,
    )
    surf_text = font.render("PLAY TRAINING COURSE", True, "#000000")
    s_train_button = Button(
        Vector(win.get_width() / 20, 600),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY TRAINING COURSE",
        False,
        "train",
        font,
    )
    surf_text = font.render("PLAY ICE MAP", True, "#000000")
    s_ice_button = Button(
        Vector(win.get_width() / 20, s_train_button.pt.y + s_train_button.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY ICE MAP",
        False,
        "ice",
        font,
    )
    surf_text = font.render("PLAY challenge", True, "#000000")
    s_tut_button = Button(
        Vector(win.get_width() / 20, s_train_button.pt.y - 20 - surf_text.get_height()),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY challenge",
        False,
        "challenge",
        font,
    )
    surf_text = font.render("BACK", True, "#000000")
    t_back_button = Button(
        Vector(win.get_width() / 20, win.get_height() * 0.05),
        surf_text.get_width(),
        surf_text.get_height(),
        "BACK",
        False,
        "selection",
        font,
    )
    surf_text = font.render("PLAY JUMPING CHALLENGE", True, "#000000")
    t_1 = Button(
        Vector(win.get_width() / 20, 400),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY JUMPING CHALLENGE",
        False,
        "1",
        font,
    )
    surf_text = font.render("PLAY DOUBLE JUMPING CHALLENGE", True, "#000000")
    t_2 = Button(
        Vector(win.get_width() / 20, t_1.pt.y + t_1.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY DOUBLE JUMPING CHALLENGE",
        False,
        "2",
        font,
    )
    surf_text = font.render("PLAY SLIDING CHALLENGE", True, "#000000")
    t_3 = Button(
        Vector(win.get_width() / 20, t_2.pt.y + t_2.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY SLIDING CHALLENGE",
        False,
        "3",
        font,
    )
    surf_text = font.render("PLAY SLIDING JUMPING CHALLENGE", True, "#000000")
    t_4 = Button(
        Vector(win.get_width() / 20, t_3.pt.y + t_3.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY SLIDING JUMPING CHALLENGE",
        False,
        "4",
        font,
    )
    surf_text = font.render("PLAY WALL BOUNCE CHALLENGE", True, "#000000")
    t_5 = Button(
        Vector(win.get_width() / 20, t_4.pt.y + t_4.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY WALL BOUNCE CHALLENGE",
        False,
        "5",
        font,
    )
    surf_text = font.render("PLAY DEATH CHALLENGE", True, "#000000")
    t_6 = Button(
        Vector(win.get_width() / 20, t_5.pt.y + t_5.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY DEATH CHALLENGE",
        False,
        "6",
        font,
    )
    surf_text = font.render("PLAY FINAL CHALLENGE", True, "#000000")
    t_7 = Button(
        Vector(win.get_width() / 20, t_6.pt.y + t_6.h + 20),
        surf_text.get_width(),
        surf_text.get_height(),
        "PLAY FINAL CHALLENGE",
        False,
        "7",
        font,
    )
    surf_text = font.render("NEXT LEVEL", True, "#000000")
    continue_button = Button(
        Vector(
            win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.475
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "NEXT LEVEL",
        False,
        "continue",
        font,
    )
    surf_text = font.render("EXIT TO DESKTOP", True, "#000000")
    p_exit_button = Button(
        Vector(win.get_width() / 2 - surf_text.get_width() / 2, win.get_height() * 0.8),
        surf_text.get_width(),
        surf_text.get_height(),
        "EXIT TO DESKTOP",
        False,
        "exit",
        font,
    )
    exit_button = Button(
        Vector(
            win.get_width() - surf_text.get_width(),
            win.get_height() - surf_text.get_height(),
        ),
        surf_text.get_width(),
        surf_text.get_height(),
        "EXIT TO DESKTOP",
        False,
        "exit",
        font,
    )

    welc_buttons = [play_button, exit_button]
    selc_buttons = [
        back_button,
        s_train_button,
        s_ice_button,
        s_tut_button,
        exit_button,
    ]
    challenge_buttons = [t_back_button, t_1, t_2, t_3, t_4, t_5, t_6, t_7, exit_button]
    challenge_fin_buttons = [f_play_button, menu_button, continue_button, p_exit_button]
    fin_buttons = [f_play_button, menu_button, p_exit_button]
    dead_buttons = [dead_button, d_menu_button, p_exit_button]
    pause_buttons = [return_button, p_menu_button, settings_button, p_exit_button]
    buttons = []

    return (
        buttons,
        welc_buttons,
        selc_buttons,
        challenge_buttons,
        challenge_fin_buttons,
        fin_buttons,
        dead_buttons,
        pause_buttons,
    )


def load_level(level: int) -> list[Surface]:
    if level == 0:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, -6500), 10, 7600, -0.1),
            Surface(Vector(1910, -6500), 10, 7600, -0.1),
            Surface(Vector(0, -7000), 1920, 500, -0.1),
            Teleporter(Vector(40, 780), 40, 20, None, 0),
            Surface(Vector(30, 760), 10, 40, -0.15),
            Surface(Vector(80, 760), 10, 40, -0.15),
            Surface(Vector(0, 570), 100, 130, -0.15),
            Surface(Vector(80, 500), 20, 70, -0.15),
            Surface(Vector(250, 795), 50, 20, -0.15, "#ff0000", True),
            Surface(Vector(200, 500), 1395, 40, -0.15),
            Surface(Vector(550, 540), 30, 225, -0.15),
            Surface(Vector(1100, 660), 500, 140, -0.15),
            Surface(Vector(1570, 540), 10, 90, -0.15),
            Surface(Vector(1700, 400), 300, 400, -0.15),
            Teleporter(Vector(25, 550), 40, 20, None, 1),
            Surface(Vector(15, 530), 10, 40, -0.15),
            Surface(Vector(65, 530), 10, 40, -0.15),
            Surface(Vector(1575, 560), 40, 20, -0.15),
            Surface(Vector(1200, 300), 100, 150, -0.15),
            Surface(Vector(1300, 400), 100, 50, -0.15),
            Surface(Vector(300, 300), 200, 200, -0.15),
            Surface(Vector(150, 400), 60, 20, -0.15),
            # End of tutorial thingy
            Surface(Vector(180, 180), 80, 20, -0.15),
            Surface(Vector(290, 100), 80, 20, -0.15),
            Surface(Vector(410, 70), 80, 20, -0.15),
            Surface(Vector(510, 40), 80, 20, -0.15),
            Surface(Vector(620, 10), 80, 20, -0.15),
            Surface(Vector(730, -80), 80, 20, -0.15),
            Surface(Vector(840, -130), 80, 20, -0.15),
            Surface(Vector(1145, -30), 65, 20, -0.2),
            Surface(Vector(1220, -120), 10, 40, -0.2),
            Surface(Vector(1240, 0), 60, 20, -0.2),
            Surface(Vector(1340, -40), 60, 20, -0.2),
            Surface(Vector(1450, -190), 60, 20, -0.15),
            Surface(Vector(1450, -310), 100, 20, -0.15),
            Surface(Vector(1700, -310), 60, 20, -0.15),
            Surface(Vector(1800, -410), 10, 60, -0.15),
            Surface(Vector(1700, -410), 100, 20, -0.15),
            Surface(Vector(1700, -500), 10, 90, -0.15),
            Surface(Vector(1845, -310), 20, 20, -0.15),
            Surface(Vector(1815, -300), 30, 10, -0.3),
            Surface(Vector(1800, -490), 20, 100, -0.15),
            Surface(Vector(1400, -490), 200, 20, -0.15),
            Surface(Vector(1500, -580), 10, 63, -0.15),
            Surface(Vector(1400, -600), 520, 20, -0.15),
            Teleporter(Vector(1800, -620), 40, 20, None, 2),
            Surface(Vector(1790, -640), 10, 40, -0.15),
            Surface(Vector(1840, -640), 10, 40, -0.15),
            Surface(Vector(600, -600), 120, 20, -0.3),
            Surface(Vector(400, -600), 100, 20, -0.15),
            Surface(Vector(150, -600), 150, 20, -0.15),
            Surface(Vector(100, -700), 100, 20, -0.15),
            Surface(Vector(180, -900), 20, 200, -0.15),
            Surface(Vector(0, -800), 50, 20, -0.15),
            Surface(Vector(0, -1000), 200, 20, -0.15),
            Surface(Vector(0, -1200), 200, 200, -0.15),
            Teleporter(Vector(30, -1220), 40, 20, None, 3),
            Surface(Vector(20, -1240), 10, 40, -0.15),
            Surface(Vector(70, -1240), 10, 40, -0.15),
            Surface(Vector(0, -1000), 20, 400, -0.15),
            Surface(Vector(320, -1050), 40, 20, -0.15),
            Surface(Vector(1600, -1050), 100, 20, -0.35),
            Surface(Vector(1560, -950), 140, 20, -0.25),
            Surface(Vector(1640, -1160), 60, 20, -0.2),
            Surface(Vector(900, -1180), 80, 20, 0.15, "#00ffff"),
            Surface(Vector(1740, -1325), 40, 200, -0.15),
            Surface(Vector(1740, -1600), 40, 200, -0.15),
            Surface(Vector(1760, -1400), 20, 105, -0.15),
            Surface(Vector(1650, -1430), 20, 20, -0.15),
            Surface(Vector(1430, -1530), 50, 20, -0.15),
            Surface(Vector(1400, -1550), 30, 40, -0.15),
            Surface(Vector(1005, -1570), 90, 20, -0.15),
            Surface(Vector(800, -1720), 700, 40, -0.15),
            Surface(Vector(550, -1600), 50, 20, -0.15),
            Surface(Vector(350, -1500), 60, 20, -0.15),
            Surface(Vector(110, -1600), 90, 20, -0.15),
            Teleporter(Vector(120, -1620), 40, 20, None, 4),
            Surface(Vector(110, -1640), 10, 40, -0.15),
            Surface(Vector(160, -1640), 10, 40, -0.15),
            Surface(Vector(1200, -1570), 70, 20, -0.15),
            Surface(Vector(800, -1570), 100, 75, -0.15),
            Surface(Vector(800, -1700), 100, 75, -0.15),
            Surface(Vector(720, -1570), 30, 20, -0.15),
            Surface(Vector(1480, -1820), 20, 100, -0.15),
            Surface(Vector(1530, -1900), 20, 40, -0.15),
            Surface(Vector(1590, -2000), 20, 40, -0.15),
            Surface(Vector(1590, -2400), 20, 40, -0.15),
            Surface(Vector(1650, -2100), 20, 40, -0.15),
            Surface(Vector(1650, -2300), 20, 40, -0.15),
            Surface(Vector(1750, -2200), 20, 40, -0.15),
            Surface(Vector(1370, -2100), 20, 40, -0.15),
            Surface(Vector(1200, -1940), 60, 20, -0.15),
            Surface(Vector(400, -1940), 120, 20, -0.15),
            Surface(Vector(300, -2100), 15, 40, -0.15),
            Surface(Vector(200, -2300), 15, 40, -0.15),
            Surface(Vector(200, -2400), 15, 40, -0.15),
            Surface(Vector(300, -2200), 15, 40, -0.15),
            Surface(Vector(150, -3600), 90, 20, -0.15),
            Teleporter(Vector(160, -3620), 40, 20, None, 5),
            Surface(Vector(150, -3640), 10, 40, -0.15),
            Surface(Vector(200, -3640), 10, 40, -0.15),
            Surface(Vector(400, -3400), 20, 900, -0.15),
            Surface(Vector(195, -2570), 10, 25, -0.15),
            Surface(Vector(350, -2620), 50, 20, -0.15),
            Surface(Vector(300, -2770), 10, 15, -0.15),
            Surface(Vector(0, -2820), 50, 20, -0.15),
            Surface(Vector(350, -2820), 50, 20, -0.15),
            Surface(Vector(100, -2920), 10, 15, -0.15),
            Surface(Vector(0, -3020), 50, 20, -0.15),
            Surface(Vector(350, -3060), 50, 20, -0.15),
            Surface(Vector(300, -3170), 10, 15, -0.15),
            Surface(Vector(175, -3320), 50, 15, -0.15),
            Surface(Vector(330, -3450), 90, 50, -0.15),
            Surface(Vector(950, -3160), 300, 20, 0.11, "#00ffff"),
            Surface(Vector(1650, -3180), 130, 20, -0.15),
            Surface(Vector(1650, -3480), 20, 250, -0.15),
            Surface(Vector(1650, -3280), 40, 20, -0.15),
            Surface(Vector(1750, -3380), 40, 20, -0.15),
            Surface(Vector(1410, -3580), 100, 20, -0.15),
            Surface(Vector(1250, -3577), 100, 20, -0.15),
            Surface(Vector(1050, -3700), 470, 20, -0.15),
            Surface(Vector(1380, -3700), 30, 85, -0.15),
            Surface(Vector(1500, -3900), 20, 200, -0.15),
            Surface(Vector(1210, -3580), 10, 20, -0.15),
            Surface(Vector(1110, -3580), 10, 20, -0.15),
            Surface(Vector(1000, -3580), 10, 20, -0.15),
            Surface(Vector(1050, -3900), 400, 20, -0.15),
            Surface(Vector(1080, -3800), 10, 100, -0.15, "#ff0000", True),
            Surface(Vector(1280, -3910), 30, 180, -0.15, "#ff0000", True),
            Surface(Vector(1380, -3800), 20, 100, -0.15, "#ff0000", True),
            Surface(Vector(1440, -3820), 20, 10, -0.15),
            Surface(Vector(380, -3960), 120, 20, -0.2),
            Surface(Vector(0, -4060), 100, 20, -0.15),
            Surface(Vector(1780, -4000), 140, 20, -0.15),
            Teleporter(Vector(1850, -4020), 40, 20, None, 6),
            Surface(Vector(1840, -4040), 10, 40, -0.15),
            Surface(Vector(1890, -4040), 10, 40, -0.15),
            Surface(Vector(380, -4160), 120, 20, -0.2),
            Surface(Vector(600, -4300), 120, 20, -0.15),
            Surface(Vector(1400, -4350), 150, 20, -0.15),
            Surface(Vector(1600, -4450), 10, 25, -0.15),
            Surface(Vector(1700, -4600), 10, 25, -0.15),
            Surface(Vector(1800, -4750), 10, 25, -0.15),
            Surface(Vector(1700, -4850), 10, 25, -0.15),
            Surface(Vector(1550, -4950), 10, 25, -0.15),
            Surface(Vector(1550, -5100), 10, 25, -0.15),
            Surface(Vector(1450, -5150), 10, 25, -0.15),
            Surface(Vector(1300, -5200), 10, 25, -0.1),
            Surface(Vector(1200, -5300), 10, 25, -0.1),
            Surface(Vector(1000, -5150), 10, 25, -0.1),
            Surface(Vector(900, -5200), 10, 25, -0.1),
            Surface(Vector(900, -5350), 10, 25, -0.1),
            Surface(Vector(900, -5500), 10, 25, -0.1),
            Surface(Vector(1050, -5500), 400, 30, -0.15),
            Surface(Vector(1200, -5625), 30, 125, -0.15, "#ff0000", True),
            Surface(Vector(1650, -5650), 50, 50, -0.15, "#888800", False, True),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 1:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
            Surface(Vector(350, 700), 20, 100, -0.15),
            Surface(Vector(600, 700), 60, 20, -0.15),
            Surface(Vector(640, 700), 20, 100, -0.15),
            Surface(Vector(700, 600), 100, 20, -0.15),
            Surface(Vector(850, 500), 100, 300, -0.15),
            Surface(Vector(1400, 740), 60, 60, -0.15, "#888800", False, True),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 2:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
            Surface(Vector(730, 650), 100, 100, -0.15),
            Surface(Vector(780, 600), 50, 50, -0.15),
            Surface(Vector(1000, 600), 50, 200, -0.15),
            Surface(Vector(1050, 700), 20, 100, -0.15),
            Surface(Vector(1000, 450), 460, 20, -0.15),
            Surface(Vector(1190, 300), 20, 150, -0.15),
            Surface(Vector(1400, 390), 60, 60, -0.15, "#888800", False, True),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 3:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
            Surface(Vector(500, 550), 20, 220, -0.15),
            Surface(Vector(750, 700), 400, 100, -0.15),
            Surface(Vector(750, 450), 400, 50, -0.15),
            Surface(Vector(900, 500), 100, 170, -0.15),
            Surface(Vector(1200, 600), 20, 40, -0.15),
            Surface(Vector(0, 550), 500, 20, -0.15),
            Surface(Vector(100, 490), 60, 60, -0.15, "#888800", False, True),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 4:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
            Surface(Vector(200, 600), 100, 150, -0.15),
            Surface(Vector(100, 700), 100, 50, -0.15),
            Surface(Vector(800, 500), 100, 20, -0.15),
            Surface(Vector(1500, 600), 200, 200, -0.15),
            Surface(Vector(1700, 700), 100, 100, -0.15),
            Surface(Vector(1600, 540), 60, 60, -0.15, "#888800", False, True),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 5:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
            Surface(Vector),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 6:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 7:
        walls = [
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, 0), 10, 1080, -0.1),
            Surface(Vector(1910, 0), 10, 1080, -0.1),
            Surface(Vector(0, -1000), 1920, 1000, -0.1),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    elif level == 8:
        walls = [
            # Surface(Vector(,), , , ),
            Surface(Vector(800, 650), 60, 20, -0.15),
            Surface(Vector(1000, 550), 60, 20, -0.15),
            Surface(Vector(1000, 400), 60, 20, -0.15),
            Surface(Vector(1000, 0), 20, 350, -0.15),
            Surface(Vector(1000, 300), 25, 20, -0.15),
            Surface(Vector(1170, 250), 20, 20, -0.15),
            Surface(Vector(1050, 100), 25, 20, -0.15),
            Surface(Vector(0, 0), 350, 20, -0.2),
            Surface(Vector(100, -150), 60, 20, -0.15),
            Surface(Vector(325, -150), 60, 20, -0.15),
            Surface(Vector(445, -300), 60, 20, -0.15),
            # Side walls
            Surface(Vector(0, 800), 1920, 580, -0.15),
            Surface(Vector(0, -50000), 10, 51080, -0.1),
            Surface(Vector(1910, -50000), 10, 51080, -0.1),
            Surface(Vector(0, -50500), 1920, 500, -0.1),
            # Surface(Vector(1650, -5050), 50, 50, -.15, "#888800", False, True),
        ]
        teleporters = []
        for wall in walls:
            if wall.is_teleport:
                wall.next_tp = wall
                teleporters.append(wall)
        return walls, teleporters
    else:
        return [], []


def main():
    # walls, teleporters = load_level(0)
    # save_map(walls)
    delta = 0.017  # second since last frame
    last_frame = time.time()

    screen = "welcome"
    previous_screen = "welcome"
    game_status = True

    # clock = pygame.time.Clock()
    start_time = datetime.datetime.now()

    win = create_window()
    fonts = create_fonts()

    times = []

    player = Player()
    # walls = load_map(0)
    walls = []
    teleporters = []
    hb_mouse = Hitbox(
        Vector(pygame.mouse.get_pos()[0] - 5, pygame.mouse.get_pos()[1] - 5),
        10,
        10,
        "#ff00ff",
    )
    (
        buttons,
        welc_buttons,
        selc_buttons,
        challenge_buttons,
        challenge_fin_buttons,
        fin_buttons,
        dead_buttons,
        pause_buttons,
    ) = create_buttons(win, fonts[2])
    maps = load_map_data()
    current_map = 0
    was_down = False
    in_challenge = False

    while game_status:
        delta = time.time() - last_frame
        last_frame = time.time()
        handle_events()
        elapsed_time = datetime.datetime.now() - start_time

        if elapsed_time == None:
            t = 0
        else:
            t = elapsed_time
        screen = handle_keys(
            screen, player, hb_mouse, delta, walls, teleporters, t, times
        )
        if screen == "welcome":
            screen, was_down = handle_mouse(screen, hb_mouse, welc_buttons, was_down)
        elif screen == "selection":
            screen, was_down = handle_mouse(screen, hb_mouse, selc_buttons, was_down)
        elif screen == "challenge":
            screen, was_down = handle_mouse(
                screen, hb_mouse, challenge_buttons, was_down
            )
        elif screen == "finished":
            if in_challenge and current_map != 7:
                f_buttons = challenge_fin_buttons
            else:
                f_buttons = fin_buttons
            screen, was_down = handle_mouse(screen, hb_mouse, f_buttons, was_down)
        elif screen == "dead":
            screen, was_down = handle_mouse(screen, hb_mouse, dead_buttons, was_down)
        elif screen == "pause":
            screen, was_down = handle_mouse(screen, hb_mouse, pause_buttons, was_down)
        else:
            screen, was_down = handle_mouse(screen, hb_mouse, buttons, was_down)

        if screen == "train":
            start_time = datetime.datetime.now()
            walls, teleporters = load_map(0)
            player = Player()
            current_map = "train"
            screen = "game"
            in_challenge = False
        elif screen == "ice":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(8)
            player = Player()
            current_map = "ice"
            screen = "game"
            in_challenge = False
        elif screen == "continue":
            start_time = datetime.datetime.now()
            current_map += 1
            walls, teleporters = load_level(current_map)
            player = Player()
            screen = "game"
            in_challenge = True
        elif screen == "1":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(1)
            player = Player()
            current_map = 1
            screen = "game"
            in_challenge = True
        elif screen == "2":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(2)
            player = Player()
            current_map = 2
            screen = "game"
            in_challenge = True
        elif screen == "3":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(3)
            player = Player()
            current_map = 3
            screen = "game"
            in_challenge = True
        elif screen == "4":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(4)
            player = Player()
            current_map = 4
            screen = "game"
            in_challenge = True
        elif screen == "5":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(5)
            player = Player()
            current_map = 5
            screen = "game"
            in_challenge = True
        elif screen == "6":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(6)
            player = Player()
            current_map = 6
            screen = "game"
            in_challenge = True
        elif screen == "7":
            start_time = datetime.datetime.now()
            walls, teleporters = load_level(7)
            player = Player()
            current_map = 7
            screen = "game"
            in_challenge = True
            # for wall in walls:
            # 	print(wall)
        if screen == "respawn":
            player = Player()
            active_tps = []
            if teleporters != []:
                next_tp = teleporters[0].next_tp
                for tp in teleporters:
                    if tp.is_active:
                        active_tps.append(tp.num)
            if current_map == "train":
                walls, teleporters = load_map(0)
            elif current_map == "ice":
                walls, teleporters = load_level(0)
            else:
                walls, teleporters = load_level(current_map)
            for i in active_tps:
                teleporters[i].is_active = True
                # if teleporters[i] == next_tp:
                # 	print("same")
                teleporters[i].next_tp = teleporters[active_tps[len(active_tps) - 1]]
            screen = "game"
        if screen == "game":
            draw_game(win, fonts[1], player, walls, hb_mouse, delta, elapsed_time)
        elif screen == "welcome":
            draw_welcome(win, fonts[0], hb_mouse, welc_buttons)
        elif screen == "selection":
            draw_selection(win, fonts[0], hb_mouse, selc_buttons)
        elif screen == "challenge":
            draw_challenge(win, fonts[0], hb_mouse, challenge_buttons)
        elif screen == "dead":
            start_time = datetime.datetime.now() - elapsed_time
            draw_dead(win, fonts[0], player, walls, hb_mouse, delta, dead_buttons)
        elif screen == "pause":
            start_time = datetime.datetime.now() - elapsed_time
            draw_pause(win, fonts[0], player, walls, hb_mouse, delta, pause_buttons)
        elif screen == "finished":
            if in_challenge and current_map != 7:
                f_buttons = challenge_fin_buttons
            else:
                f_buttons = fin_buttons
            draw_finished(win, fonts[0], player, walls, hb_mouse, delta, f_buttons)

        if screen == "exit":
            pygame.quit()
            quit()
        pygame.display.flip()

        # clock.tick_busy_loop(200)

        # print("Delta: %1.3f\tFPS: %4.2f" % (delta, 1/delta))


main()
