from __future__ import annotations # for type hints
import pygame # graphics library
from pygame.locals import * # for keyboard input (ex: 'K_w')
import math


class Vector(): # vec
	def __init__(self, x: float, y: float):
		self._x: float = x
		self._y: float = y

	def __str__(self) -> str:
		return "<%f, %f>" % (self.get_x(), self.get_y())

	def get_x(self) -> float:
		return self._x
	def set_x(self, x: float) -> None:
		self._x = x
	def get_y(self) -> float:
		return self._y
	def set_y(self, y: float) -> None:
		self._y = y

	def calc_length(self) -> float:
		return math.sqrt(self.get_x() ** 2 + self.get_y() ** 2)

	def add(self, vec_other: Vector) -> Vector:
		return Vector(self.get_x() + vec_other.get_x(), self.get_y() + vec_other.get_y())

	def apply(self, vec_other: Vector) -> None:
		self.set_x(self.get_x() + vec_other.get_x())
		self.set_y(self.get_y() + vec_other.get_y())

	def subtract(self, vec_other: Vector) -> Vector:
		return Vector(self.get_x() - vec_other.get_x(), self.get_y() - vec_other.get_y())

	def scalar(self, s: float) -> Vector:
		return Vector(self.get_x() * s, self.get_y() * s)

	def scale(self, length: float) -> Vector:
		try:
			return Vector(self.get_x() * length/self.calc_length(), self.get_y() * length/self.calc_length())
		except ZeroDivisionError:
			return Vector(0, 0)


class Hitbox(): # hb
	def __init__(self, pt: Vector, w: float, h: float, color: str = "#ffffff"):
		self._pt: Vector = pt
		self._w: float = w
		self._h: float = h
		self._color: str = color

	def __str__(self) -> str:
		return "(%s, %f, %f)" % (self.get_pt(), self.get_w(), self.get_h())

	def get_pt(self) -> Vector:
		return self._pt
	def get_center(self) -> Vector:
		return Vector(self.get_pt().get_x() + self.get_w()/2, self.get_pt().get_y() + self.get_h()/2)
	def set_pt(self, pt: Vector) -> None:
		self._pt = pt
	def get_w(self) -> float:
		return self._w
	def set_w(self, w: float) -> None:
		self._w = w
	def get_h(self) -> float:
		return self._h
	def set_h(self, h: float) -> None:
		self._h = h
	def get_rect(self) -> pygame.Rect:
		return pygame.Rect(self.get_pt().get_x(), self.get_pt().get_y(), self.get_w(), self.get_h())
	def get_color(self) -> str:
		return self._color
	def set_color(self, color: str) -> None:
		self._color = color

	def check_collide(self, hb_other: Hitbox) -> bool:
		return (
			self.get_pt().get_x() < hb_other.get_pt().get_x() + hb_other.get_w()
			and hb_other.get_pt().get_x() < self.get_pt().get_x() + self.get_w()
			and self.get_pt().get_y() < hb_other.get_pt().get_y() + hb_other.get_h()
			and hb_other.get_pt().get_y() < self.get_pt().get_y() + self.get_h()
		)

	def draw(self, win: pygame.Surface) -> None:
		pygame.draw.rect(win, self.get_color(), self.get_rect())

class HitboxPart(Hitbox): # hbp
	def __init__(self, pt: Vector, vec_offset: Vector, w: float, h: float, color: str = "#ffffff"):
		super().__init__(pt, w, h, color)
		self._vec_offset: Vector = vec_offset

	def __str__(self) -> str:
		return "Hitbox Part: %s" % super().__str__()

	def get_vec_offset(self) -> Vector:
		return self._vec_offset
	def set_vec_offset(self, vec_offset: Vector) -> None:
		self._vec_offset = vec_offset

	def update_pt_from_master(self, ahb_master: AdvancedHitbox) -> None:
		self.set_pt(ahb_master.get_pt().add(self.get_vec_offset()))

class AdvancedHitbox(Hitbox): # ahb
	def __init__(self, pt: Vector, w: float, h: float, color: str = "#ffffff"):
		super().__init__(pt, w, h, color)
		self._hbps: list[HitboxPart] = []

	def __str__(self) -> str:
		return "Advanced Hitbox: %s" % super().__str__()

	def get_hbps(self) -> list[HitboxPart]:
		return self._hbps
	def add_hbp(self, hbp: HitboxPart) -> None:
		self.get_hbs().append(hbp)

	def check_collisions(self, hb_other: Hitbox) -> bool:
		for hbp in self.get_hbps():
			if hbp.check_collide(hb_other):
				return True
		return False

	def check_advanced_collisions(self, ahb_other: AdvancedHitbox) -> bool:
		for hbp_self in self.get_hbs():
			for hbp_other in ahb_other.get_hbs():
				if hbp_self.check_collide(hbp_other):
					return True
		return False

	def update_hbps(self) -> None:
		for hbp in self.get_hbps():
			hbp.update_pt_from_master(self)

	def draw(self, win: pygame.Surface) -> None:
		super().draw(win)
		for hbp in self.get_hbps():
			hbp.draw(win)

class Player(AdvancedHitbox): # p
	def __init__(self):
		super().__init__(Vector(0, 0), 40, 40, "#00ff00")
		self._ms: float = 10

	def __str__(self) -> str:
		return "Player: %s" % super().__str__()

	def get_ms(self) -> float:
		return self._ms
	def set_ms(self, ms):
		self._ms = ms

	def handle_keys(self, keys_down: list[bool], delta: float) -> None:
		vec_move = Vector(0, 0)
		if keys_down[K_w]:
			vec_move.set_y(-1)
		elif keys_down[K_s]:
			vec_move.set_y(1)
		elif keys_down[K_a]:
			vec_move.set_x(-1)
		elif keys_down[K_d]:
			vec_move.set_x(1)
		vec_move = vec_move.scale(self.get_ms() * delta)
		self.get_pt().apply(vec_move)

	# def draw(self, win: pygame.Surface, color: str = "#00ff00") -> None:
	# 	pygame.draw.rect(win, color, self.get_rect())