import math
import pygame

class Vector(): # vec
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def __str__(self):
		return "<%f, %f>" % (self.x, self.y)

	def get_x(self) -> float:
		return self.x

	def get_y(self) -> float:
		return self.y

	def set_x(self, x: float):
		self.x = x

	def set_y(self, y: float):
		self.y = y

	def calc_length(self) -> float:
		return math.sqrt(self.get_x() * self.get_x() + self.get_y() * self.get_y())

	def apply(self, vec_other: Vector) -> None:
		self.set_x(self.get_x() + vec_other.get_x())
		self.set_y(self.get_y() + vec_other.get_y())

	def add(self, vec_other: Vector) -> Vector:
		return Vector(self.x + vec_other.get_x(), self.y + vec_other.get_y())

	def subtract(self, vec_other: Vector) -> Vector:
		return Vector(self.x - vec_other.get_x(), self.y - vec_other.get_y())

	def scalar(self, s: float) -> None:
		self.x *= s
		self.y *= s

	def scale(self, length: float) -> None:
		currentLen = self.calc_length()
		try:
			self.x *= length / currentLen
			self.y *= length / currentLen
		except ZeroDivisionError:
			print("Cannot scale vector from zero")

class Hitbox(): # hb
	def __init__(self, pt: Vector, w: float, h: float):
		self.pt = pt
		self.w = w
		self.h = h

	def __str__(self):
		return self.pt

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
			self.pt.get_x() < hb_other.get_pt().get_x() + hb_other.get_w()
			and hb_other.get_pt().get_x() < self.pt.get_x() + self.w
			and self.pt.y < hb_other.get_pt().get_y() + hb_other.get_y()
			and hb_other.get_pt().get_y() < self.pt.get_y() + self.h
		)

	def draw(self, win: Surface, color: str = "#00ff00") -> None:
		pygame.draw.rect(self.get_rect())
