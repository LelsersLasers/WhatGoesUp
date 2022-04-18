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
	def get_tuple(self) -> tuple[float, float]:
		return (self.get_x(), self.get_y())
	def get_angle(self) -> float:
		try:
			angle = math.atan(self.get_y()/self.get_x()) * 180/math.pi
			if self.get_x() < 0: angle += 180
		except ZeroDivisionError:
			angle = 90 if self.get_y() > 0 else 270
		return angle % 360
	def set_angle(self, angle: float) -> None:
		current_length = self.calc_length()
		self.set_x(math.cos(angle * math.pi/180))
		self.set_y(math.sin(angle * math.pi/180))
		self.set_vec(self.scale(current_length))
	def set_vec(self, vec_other: Vector) -> None:
		self.set_x(vec_other.get_x())
		self.set_y(vec_other.get_y())

	def calc_length(self) -> float:
		return math.sqrt(self.get_x() ** 2 + self.get_y() ** 2)

	def add(self, vec_other: Vector) -> Vector:
		return Vector(self.get_x() + vec_other.get_x(), self.get_y() + vec_other.get_y())

	def apply(self, vec_other: Vector) -> None:
		self.set_vec(self.add(vec_other))

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
		self.get_hbps().append(hbp)

	def check_collisions(self, hb_other: Hitbox) -> bool:
		for hbp in self.get_hbps():
			if hbp.check_collide(hb_other):
				return True
		return False

	def check_advanced_collisions(self, ahb_other: AdvancedHitbox) -> bool:
		for hbp_self in self.get_hbps():
			for hbp_other in ahb_other.get_hbps():
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


class Combatant(AdvancedHitbox):
	def __init__(self, pt: Vector, w: float, h: float, hp: float, damage: float, ms: float, color: str = "#ffffff"):
		super().__init__(pt, w, h, color)
		self._hp: float = hp
		self._damage: float = damage
		self._ms: float = ms

	def __str__(self) -> str:
		return "Combatant: %s" % super().__str__()

	def get_hp(self) -> float:
		return self._hp
	def set_hp(self, hp: float) -> None:
		self._hp = hp
	def get_damage(self) -> float:
		return self._damage
	def set_damage(self, damage: float) -> None:
		self._damage = damage
	def get_ms(self) -> float:
		return self._ms
	def set_ms(self, ms: float) -> None:
		self._ms = ms


class Player(Combatant): # p
	def __init__(self):
		super().__init__(Vector(0, 0), 40, 40, 100, 20, 500, "#00ff00")
		self.add_hbp(HitboxPart(Vector(-10, -10), Vector(-10, -10), 25, 25))
		self.add_hbp(HitboxPart(Vector(25, -10), Vector(25, -10), 25, 25))
		self.add_hbp(HitboxPart(Vector(-10, 25), Vector(-10, 25), 25, 25))
		self.add_hbp(HitboxPart(Vector(25, 25), Vector(25, 25), 25, 25))

		self._inventory: list[Item] = [Item(self, "Sword", "It is a sword")]
		self._active_item_index: int = 0

	def __str__(self) -> str:
		return "Player: %s" % super().__str__()

	def get_inventory(self) -> list[Item]:
		return self._inventory
	def add_item(self, item: Item) -> None:
		self.get_inventory().append(item)
	def get_active_item_index(self) -> int:
		return self._active_item_index
	def set_active_item_index(self, index: int) -> None:
		self._active_item_index = index
	def get_active_item(self) -> Item:
		return self.get_inventory()[self.get_active_item_index()]

	def handle_keys(self, keys_down: list[bool], delta: float) -> None:
		vec_move = Vector(0, 0)
		if keys_down[K_w]:
			vec_move.set_y(-1)
		if keys_down[K_s]:
			vec_move.set_y(1)
		if keys_down[K_a]:
			vec_move.set_x(-1)
		if keys_down[K_d]:
			vec_move.set_x(1)
		self.get_pt().apply(vec_move.scale(self.get_ms() * delta))
		self.update_hbps()

	def draw(self, win: pygame.Surface, color: str = "#00ff00") -> None:
		super().draw(win)
		self.get_active_item().update_pt()
		self.get_active_item().draw(win)




class Enemy(Combatant): # enemy
	def __init__(self, pt: Vector, w: float, h: float, target: Player, vision_range: float, level: int, color: str = "#ff0000"):
		super().__init__(pt, w, h, -1, -1, -1, color)
		self._target: Player = target
		self._vision_range: float = vision_range
		self._cone_angle: float = 70 # degrees
		self._vision_direction: float = 0 # degrees
		self._level = level
		self.set_base_stats()

	def set_base_stats(self) -> None:
		self.set_hp(50 + self.get_level() * 10)
		self.set_damage(5 + self.get_level() * 5)
		self.set_ms(350 + self.get_level() * 10)

	def get_target(self) -> Player:
		return self._target
	def set_target(self, target: Player):
		self._target = target
	def get_vision_range(self) -> float:
		return self._vision_range
	def set_vision_range(self, vision_range: float) -> None:
		self._vision_range = vision_range
	def get_aggro_range(self) -> float:
		return self.get_vision_range()/2
	def get_cone_angle(self) -> float:
		return self._cone_angle
	def set_cone_angle(self, cone_angle: float) -> None:
		self._cone_angle = cone_angle
	def get_vision_direction(self) -> float:
		return self._vision_direction
	def set_vision_direction(self, vision_direction: float) -> None:
		self._vision_direction = vision_direction
	def get_level(self) -> int:
		return self._level
	def get_vec_to_target(self) -> Vector:
		return self.get_target().get_center().subtract(self.get_center())
	def get_top_of_vision_cone(self) -> Vector:
		vec = Vector(self.get_vision_range(), 0)
		vec.set_angle(self.get_vision_direction() - self.get_cone_angle()/2)
		return vec
	def get_bottom_of_vision_cone(self) -> Vector:
		vec = Vector(self.get_vision_range(), 0)
		vec.set_angle(self.get_vision_direction() + self.get_cone_angle()/2)
		return vec

	def check_vision_range(self) -> bool:
		vec_dif = self.get_target().get_center().subtract(self.get_center())
		return vec_dif.calc_length() <= self.get_vision_range()

	def check_aggro_range(self) -> bool:
		vec_dif = self.get_target().get_center().subtract(self.get_center())
		return vec_dif.calc_length() <= self.get_aggro_range()

	def check_vision(self) -> bool:
		if not self.check_vision_range():
			return False
		angle_to_target = self.get_vec_to_target().get_angle()
		angle_start = self.get_top_of_vision_cone().get_angle()
		angle_end = self.get_bottom_of_vision_cone().get_angle()

		if angle_end < angle_start:
			angle_end += 360
		if angle_to_target >= angle_start and angle_to_target <= angle_end:
			return True
		return angle_to_target >= angle_start - 360 and angle_to_target <= angle_end - 360

	def update(self, delta: float) -> None:
		if self.check_aggro_range() or self.check_vision():
			vec_move = self.get_vec_to_target().scale(self.get_ms() * delta)
			self.get_pt().apply(vec_move)
			self.set_vision_direction(vec_move.get_angle())


	def draw(self, win: pygame.Surface) -> None:
		color = self.get_color()
		if self.get_target().check_collisions(self):
			color = "#0000ff"
		elif self.check_aggro_range() or self.check_vision():
			color = "#00ff00"

		pygame.draw.circle(win, color, self.get_center().get_tuple(), self.get_aggro_range(), 3)

		vec_look_1 = self.get_top_of_vision_cone()
		vec_look_1.apply(self.get_center())
		vec_look_2 = self.get_bottom_of_vision_cone()
		vec_look_2.apply(self.get_center())

		pygame.draw.line(win, color, self.get_center().get_tuple(), vec_look_1.get_tuple(), 3)
		pygame.draw.line(win, color, self.get_center().get_tuple(), vec_look_2.get_tuple(), 3)

		pygame.draw.line(win, color, self.get_center().get_tuple(), self.get_target().get_center().get_tuple(), 3)

		super().draw(win)

class Item(AdvancedHitbox): # item
	def __init__(self, player: Player, name: str, description: str):
		super().__init__(player.get_center(), 10, 10, "#0000ff")
		self._player: Player = player
		self._name: str = name
		self._description: str = description

	def get_player(self) -> Player:
		return self._player
	def get_name(self) -> str:
		return self._name
	def set_name(self, name: str) -> None:
		self._name = name
	def get_description(self) -> str:
		return self._description
	def set_description(self, description: str) -> None:
		self._description = description

	def update_pt(self) -> None:
		self.set_pt(self.get_player().get_center())

class Weapon(Item):
	def __init__(self, player: Player, name: str, description: str, damage: float, fire_rate: float, range: float):
		super().init(player, name, description)
		self._damage: float = damage
		self._fire_rate: float = fire_rate # attacks/sec
		self._range: float = range

	def get_damage(self) -> float:
		return self._damage
	def set_damage(self, damage: float) -> None:
		self._damage = damage
	def get_fire_rate(self) -> float:
		return self._fire_rate
	def set_fire_rate(self, fire_rate: float) -> None:
		self._fire_rate = fire_rate
	def get_range(self) -> float:
		return self._range
	def set_range(self, range: float):
		self._range = range

class MeleeWeapon(Weapon):
	def __init__(self, player: Player, name: str, description: str, damage: float, fire_rate: float, range: float):
		super().__init__(player, name, description, damage, fire_rate, range)

class RangedWeapon(Weapon):
	def __init__(self, player: Player, name: str, description: str, damage: float, fire_rate: float, range: float):
		super().__init__(player, name, description, damage, fire_rate, range)

class MagicWeapon(Weapon):
	def __init__(self, player: Player, name: str, description: str, damage: float, fire_rate: float, range: float):
		super().__init__(player, name, description, damage, fire_rate, range)
