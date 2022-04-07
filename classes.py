from __future__ import annotations
import math
import pygame

class Vector(): # vec
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def get_x(self) -> float:
		return self.x

	def get_y(self) -> float:
		return self.y

	def set_x(self, x: float):
		self.x = x

	def set_y(self, y: float):
		self.y = y

	def __str__(self):
		return "<%f, %f>" % (self.get_x(), self.get_y())

	def calc_length(self) -> float:
		return math.sqrt(self.get_x() * self.get_x() + self.get_y() * self.get_y())

	def add(self, vec_other: Vector) -> Vector:
		return Vector(self.get_x() + vec_other.get_x(), self.get_y() + vec_other.get_y())

	def apply(self, vec_other: Vector) -> None:
		# self.set_x(self.get_x() + vec_other.get_x())
		# self.set_y(self.get_y() + vec_other.get_y())
		self = self.add(vec_other)

	def subtract(self, vec_other: Vector) -> Vector:
		return Vector(self.get_x() - vec_other.get_x(), self.get_y() - vec_other.get_y())

	def scalar(self, s: float) -> Vector:
		return Vector(self.get_x() * s, self.get_y() * s)

	def scale(self, length: float) -> Vector:
		try:
			return Vector(self.get_x() * length/self.calc_length(), self.get_y() * length/self.calc_length())
		except ZeroDivisionError:
			print("Cannot scale vector from zero")
			return Vector(-1, -1)

class Hitbox(): # hb
	def __init__(self, pt: Vector, w: float, h: float):
		self.pt = pt
		self.w = w
		self.h = h

	def __str__(self):
		return "(%s, %f, %f)" % (self.get_pt(), self.get_w(), self.get_h())

	def get_pt(self) -> Vector:
		return self.pt

	def get_w(self) -> float:
		return self.w

	def get_h(self) -> float:
		return self.h

	def get_rect(self) -> pygame.Rect:
		return pygame.Rect(self.pt.get_x(), self.pt.get_y(), self.w, self.h)

	def set_pt(self, pt: Vector) -> None:
		self.pt = pt

	def set_w(self, w: float) -> None:
		self.w = w

	def set_h(self, h: float) -> None:
		self.h = h

	def checkCollide(self, hb_other: Hitbox) -> bool:
		return (
			self.get_pt().get_x() < hb_other.get_pt().get_x() + hb_other.get_w()
			and hb_other.get_pt().get_x() < self.get_pt().get_x() + self.get_w()
			and self.get_pt().get_y() < hb_other.get_pt().get_y() + hb_other.get_y()
			and hb_other.get_pt().get_y() < self.pt.get_y() + self.get_h()
		)

	def draw(self, win: pygame.Surface, color: str = "#00ff00") -> None:
		pygame.draw.rect(win, color, self.get_rect())