import numpy as np
from ..Vector import Vector as V

class Line:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c


class LineSeg:
	def __init__(self, pos0=(0, 0), pos1=(0, 0)):
		self.pos0 = V.Vector(pos0[0], pos0[1])
		self.pos1 = V.Vector(pos1[0], pos1[1])
		self.a = self.pos1.y - self.pos0.y
		self.b = self.pos0.x - self.pos1.x
		self.c = self.pos0.x * (self.pos0.y - self.pos1.y) + self.pos0.y * (self.pos1.x - self.pos0.x)
