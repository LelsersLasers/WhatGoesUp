from __future__ import annotations  # for type hints
import pygame  # graphics library
from pygame.locals import *  # for keyboard input (ex: 'K_w')
import math
import copy


class Toggle:
    def __init__(self):
        self.was_down = False

    def down(self, condition: bool) -> bool:
        if not self.was_down and condition:
            self.was_down = True
            return True
        elif not condition:
            self.was_down = False
        return False


class Vector:  # vec
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __str__(self) -> str:
        return "<%f, %f>" % (self.x, self.y)

    def set_vec(self, vec: Vector) -> None:
        self.x = vec.x
        self.y = vec.y

    def get_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def get_angle(self) -> float:
        try:
            angle = math.atan(self.y / self.x) * 180 / math.pi
            if self.x < 0:
                angle += 180
        except ZeroDivisionError:
            angle = 90 if self.y > 0 else 270
        return angle % 360

    def set_angle(self, angle: float) -> None:
        current_length = self.calc_length()
        self.x = math.cos(angle * math.pi / 180)
        self.y = math.sin(angle * math.pi / 180)
        self.set_vec(self.scale(current_length))

    def calc_length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def add(self, vec: Vector) -> Vector:
        return Vector(self.x + vec.x, self.y + vec.y)

    def subtract(self, vec: Vector) -> Vector:
        return self.add(vec.scalar(-1))

    def apply(self, vec: Vector) -> None:
        self.set_vec(self.add(vec))

    def scalar(self, s: float) -> Vector:
        return Vector(self.x * s, self.y * s)

    def scale(self, length: float) -> Vector:
        current_length = self.calc_length()
        if current_length == 0:
            return Vector(0, 0)
        return self.scalar(length / current_length)


class Hitbox:  # hb
    def __init__(self, pt: Vector, w: float, h: float, color: str = "#ffffff"):
        self.pt: Vector = pt
        self.w: float = w
        self.h: float = h
        self.color: str = color

    def __str__(self) -> str:
        return "(%s, %f, %f)" % (self.pt, self.w, self.h)

    # def get_center(self) -> Vector:
    # 	return Vector(self.pt.x + self.w/2, self.pt.y + self.h/2)
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pt.x, self.pt.y, self.w, self.h)

    def check_collide(self, hb: Hitbox) -> bool:
        return (
            self.pt.x < hb.pt.x + hb.w
            and hb.pt.x < self.pt.x + self.w
            and self.pt.y < hb.pt.y + hb.h
            and hb.pt.y < self.pt.y + self.h
        )

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.rect(win, self.color, self.get_rect())


class HitboxPart(Hitbox):  # hbp
    def __init__(
        self, pt: Vector, vec_offset: Vector, w: float, h: float, color: str = "#ffffff"
    ):
        super().__init__(pt, w, h, color)
        self.vec_offset: Vector = vec_offset

    def __str__(self) -> str:
        return "Hitbox Part: %s" % super().__str__()

    def update_pt_from_master(self, ahb_master: AdvancedHitbox) -> None:
        self.PT = ahb_master.pt.add(self.vec_offset)


class AdvancedHitbox(Hitbox):  # ahb
    def __init__(self, pt: Vector, w: float, h: float, color: str = "#ffffff"):
        super().__init__(pt, w, h, color)
        self.hbps: list[HitboxPart] = []

    def __str__(self) -> str:
        return "Advanced Hitbox: %s" % super().__str__()

    def add_hbp(self, hbp: HitboxPart) -> None:
        self.hbps.append(hbp)

    def check_collisions(self, hb: Hitbox) -> bool:
        for hbp in self.hbps:
            if hbp.check_collide(hb):
                return True
        return False

    def check_advanced_collisions(self, ahb: AdvancedHitbox) -> bool:
        for hbp_self in self.hbps:
            for hbp_other in ahb.hbps:
                if hbp_self.check_collide(hbp_other):
                    return True
        return False

    def update_hbps(self) -> None:
        for hbp in self.hbps:
            hbp.update_pt_from_master(self)

    # def draw(self, win: pygame.Surface) -> None:
    # 	super().draw(win)
    # 	for hbp in self.hbps():
    # 		hbp.draw(win)


class Player(AdvancedHitbox):  # p
    def __init__(self):
        super().__init__(Vector(100, 760), 25, 40, "#00ff00")
        self.add_hbp(HitboxPart(Vector(100, 760), Vector(0, 0), 25, 40))
        # self.add_hbp(HitboxPart(Vector(150, 855), Vector(0, 10), 25, 25))
        # self.add_hbp(HitboxPart(Vector(150, 875), Vector(2.5, 35), 20, 10))

        self.ms: float = 200
        self.terminal_vel: float = 250
        self.vec_move: Vector = Vector(0, 0)
        self.is_grounded = False
        self.is_sliding = False
        self.is_stuck = False
        self.can_double_jump = True
        self.space_was_down = False  # space bar was down - USE TOGGLE!!!
        self.jumped_while_sliding = False
        self.is_alive = True
        self.is_finished = False

        self.can_fly = False
        self.p_toggle: Toggle = Toggle()

    def __str__(self) -> str:
        return "Player: %s" % super().__str__()

    def set_is_sliding(
        self,
        is_sliding: bool,
        walls: list[Surface],
        delta: float,
        keys_down: list[bool],
    ) -> None:
        p_temp = copy.deepcopy(self)
        if not self.is_sliding and is_sliding:
            p_temp.change_dimensions()
            can_slide = True
            for wall in walls:
                if p_temp.check_collisions(wall):
                    can_slide = False
            if can_slide:
                self.change_dimensions()
                if keys_down[K_d]:
                    self.vec_move.x = 800
                elif keys_down[K_a]:
                    self.vec_move.x = -800
            self.is_sliding = can_slide
        elif self.is_sliding and not is_sliding:
            if self.vec_move.x < 0:
                p_temp.pt.x = p_temp.pt.x + p_temp.w - self.h
                hb = p_temp.hbps[0]
                hb.pt.x = hb.pt.x + hb.w - self.h
            p_temp.change_dimensions()
            can_stand = True
            for wall in walls:
                if p_temp.check_collisions(wall):
                    can_stand = False
            if can_stand:
                if self.vec_move.x < 0:
                    self.pt.x = self.pt.x + self.w - self.h
                    hb = self.hbps[0]
                    hb.pt.x = hb.pt.x + hb.w - self.h
                self.change_dimensions()
                self.is_stuck = False
            else:
                self.is_stuck = True
            self.is_sliding = not can_stand

    def change_dimensions(self) -> None:
        temp = self.h
        self.h = self.w
        self.w = temp
        self.pt.y = self.pt.y + self.w - self.h
        can_slide = True  # wat this do?
        for hb in self.hbps:
            hb.h, hb.w = hb.w, hb.h
            hb.pt.y = hb.pt.y + hb.w - hb.h

    def handle_keys(
        self,
        keys_down: list[bool],
        hb_mouse: Hitbox,
        delta: float,
        walls: list[Surface],
        teleporters: list[Teleporter],
    ) -> None:
        if self.p_toggle.down(keys_down[K_p]):
            self.can_fly = not self.can_fly
        if not self.can_fly:
            self.vec_move.y = self.vec_move.y + 1000 * delta
            # if self.vec_move.y > self.get_terminal_vel():
            # 	self.vec_move.set_y(self.get_terminal_vel())
            if (
                keys_down[K_SPACE]
                and self.is_grounded
                and not self.jumped_while_sliding
            ):
                self.vec_move.y -= 500
                self.is_grounded = False
                self.space_was_down = False
                if self.is_sliding:
                    self.jumped_while_sliding = True
            elif (
                keys_down[K_SPACE]
                and not self.is_grounded
                and self.can_double_jump
                and self.space_was_down
                and not self.jumped_while_sliding
            ):
                self.vec_move.y = self.vec_move.y - 350
                self.can_double_jump = False
                self.space_was_down = False
                if self.is_sliding:
                    self.jumped_while_sliding = True
            elif not keys_down[K_SPACE] and not self.space_was_down:
                self.space_was_down = True
            if keys_down[K_a] and not self.is_sliding:
                move = -self.ms
                if not self.is_grounded:
                    move *= 0.45
                self.vec_move.x = move
            if keys_down[K_d] and not self.is_sliding:
                move = self.ms
                if not self.is_grounded:
                    move *= 0.45
                self.vec_move.x = move
            if keys_down[K_a] and self.is_sliding and self.is_stuck:
                self.set_is_sliding(False, walls, delta, keys_down)
                self.vec_move.x = -self.ms
            if keys_down[K_d] and self.is_sliding and self.is_stuck:
                self.set_is_sliding(False, walls, delta, keys_down)
                self.vec_move.x = self.ms
            if keys_down[K_LCTRL] and self.is_grounded and not self.is_sliding:
                self.set_is_sliding(True, walls, delta, keys_down)
        else:
            if keys_down[K_SPACE]:
                self.vec_move.y = self.vec_move.y - 100 * delta
            elif keys_down[K_LCTRL]:
                self.vec_move.y = self.vec_move.y + 100 * delta
            else:
                self.vec_move.y = 0
            if keys_down[K_a]:
                self.vec_move.x = self.vec_move.x - 100 * delta
            elif keys_down[K_d]:
                move = self.ms * delta
                if not self.is_grounded:
                    move *= 0.5
                self.vec_move.x = self.vec_move.x + 100 * delta
            else:
                self.vec_move.x = 0
        # force = (keys_down[K_d] * self.get_ms() + keys_down[K_a] * -1 * self.get_ms())
        p_temp = copy.deepcopy(self)

        p_temp.pt.y = p_temp.pt.y + p_temp.vec_move.y * delta
        p_temp.update_hbps()
        is_grounded = False
        for wall in walls:
            if p_temp.check_collisions(wall):
                if wall.is_teleport:
                    if wall.is_active:
                        if wall.next_tp() != wall:
                            wall.teleport(self, walls)
                    elif wall.num != 0 and not teleporters[0].is_active():
                        # could make wall and teleporters[0] point to the same object?
                        wall.activate()
                        teleporters[0].activate()
                        for tp in teleporters:
                            if tp.is_active:
                                tp.next_tp = wall
                    elif wall.num != 0:
                        wall.set_is_active(True)
                        if wall.num > teleporters[0].next_tp.num:
                            for tp in teleporters:
                                if tp.is_active:
                                    tp.next_tp = wall
                        else:
                            wall.next_tp = teleporters[0].next_tp
                elif wall.can_kill():
                    self.is_alive = False
                    break
                elif wall.is_finish:
                    self.is_finished = True
                    break
                p_temp.pt.y = p_temp.pt.y - p_temp.vec_move.y * delta
                if self.vec_move.y > 0:
                    # self.vec_move.set_x(0)
                    is_grounded = True
                    # if self.get_is_sliding():
                    # 	friction_reduction = abs(self.vec_move.x) - (abs(self.vec_move.x) * wall.get_friction() * 108 * delta)
                    # else:
                    # 	friction_reduction = abs(self.vec_move.x) - (abs(self.vec_move.x) * wall.get_friction() * 100 * delta)
                    self.vec_move.x = (
                        self.vec_move.x + (self.vec_move.x * wall.friction) * 60 * delta
                    )
                    if abs(self.vec_move.x) < 0.08:
                        self.set_is_sliding(False, walls, delta, keys_down)
                        self.vec_move.x = 0
                        self.jumped_while_sliding = False
                    if self.vec_move.y > 1000:
                        print("Splat sfx")
                self.vec_move.y = 0
                break
        p_temp.pt.x = p_temp.pt.x + p_temp.vec_move.x * delta
        p_temp.update_hbps()
        if self.is_alive or self.is_finished:
            for wall in walls:
                if p_temp.check_collisions(wall):
                    if wall.can_kill:
                        self.is_alive = False
                        break
                    if wall.is_finish:
                        self.is_finished = True
                        break
                    p_temp.pt.x = p_temp.pt.x - p_temp.vec_move.x
                    if p_temp.is_sliding and not p_temp.is_grounded:
                        self.vec_move.x *= -0.3
                    else:
                        self.vec_move.x = 0
                    break
        self.is_grounded = is_grounded
        if is_grounded:
            self.can_double_jump = True

        self.pt.x = self.pt.x + self.vec_move.x * delta
        for wall in walls:
            wall.pt.y = wall.pt.y - self.vec_move.y * delta
        self.update_hbps()

    def draw(self, win: pygame.Surface, color: str = "#00ff00") -> None:
        super().draw(win)


class Surface(Hitbox):
    # much exxessive to do it with multiple boolean variables - use an enum or id string instead
    def __init__(
        self,
        pt: Vector,
        w: float,
        h: float,
        friction: float,
        color: str = "#000000",
        can_kill: bool = False,
        is_finish: bool = False,
        is_teleport: bool = False,
    ):
        super().__init__(pt, w, h, color)
        self.friction = friction
        self.can_kill = can_kill
        self.is_finish = is_finish
        self.is_teleport = is_teleport


class Teleporter(Surface):
    def __init__(
        self,
        pt: Vector,
        w: float,
        h: float,
        next_tp: Teleporter,
        num: int,
        friction: float = -0.15,
        color: str = "#7c7c7c",
    ):
        super().__init__(pt, w, h, friction, color, False, False, True)
        self.next_tp = next_tp
        self.is_active = False
        self.num = num
        self.not_active_color = "#7c7c7c"
        self.active_color = "#990099"

    def activate(self) -> None:
        self.is_active = True
        self.color = self.active_color

    def calc_height(self) -> float:
        dis = self.next_tp.pt.y - self.pt.y
        return dis

    def teleport(self, player: Player, walls: list[Surface]) -> None:
        player.pt.x = self.next_tp.pt.x + (self.next_tp.w / 2) - (player.w / 2)
        player.vec_move = Vector(0, 0)
        dif = self.calc_height()
        print("teleport sfx")
        for wall in walls:
            wall.pt.y = wall.pt.y - dif


class Button(Hitbox):
    def __init__(
        self,
        pt: Vector,
        w: float,
        h: float,
        text: str,
        has_border: bool,
        location: str,
        font: pygame.font,
        color: str = "#ff0000",
    ):
        super().__init__(pt, w, h, color)
        self.text = text
        self.has_border = has_border
        self.next_loc = location
        self.font = font

    def draw(self, win: pygame.Surface):
        # super().draw(win)
        # 40 font
        font = self.font
        surf_text = font.render(self.text, True, self.color)
        win.blit(surf_text, (self.pt.get_tuple()))


class Map:
    def __init__(self, name: str, size: str, difficultly: str, description: str):
        self.vert_offset = 0
        self.name = name
        self.size = size
        self.difficulty = difficultly
        self.description = description

    def add_vert_offset(self, vert_offset: float) -> None:
        self.vert_offset += vert_offset
