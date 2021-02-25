import numpy as np
from ..Vector import *
from .BaseGeometry import *


class Geometry:
	def __init__(self):
		self.type=None
		pass


class Circle(Geometry):
	def __init__(self, pos, radius):
		super().__init__()
		self.type = "circle"
		self.pos = pos
		self.radius = radius


class Ellipse(Geometry):
	def __init__(self, pos=(0, 0), r1=10, r2=10, res=20):
		super().__init__()
		self.type = "ellipse"
		self.centre = Vector(pos[0], pos[1])
		self.radX = r1
		self.radY = r2
		self.res = res
		self.vertices = [(self.centre.x + self.radX * np.cos(theta), self.centre.y + self.radY * np.sin(theta)) for
		                 theta in np.linspace(0, 2 * np.pi, res + 1)[:-1]]
		print(np.linspace(0, 360, res + 1)[:-1])
		self.poly = Polygon(self.vertices)
		self.AABB = [Vector(self.centre.x - self.radX, self.centre.y - self.radY),
		             Vector(self.centre.x + self.radX, self.centre.y + self.radY)]


class Polygon(Geometry):
	def __init__(self, posList=None, closed=True):
		super().__init__()
		self.type = "polygon"
		if posList is None:
			posList = []
		self.posList = posList
		self.vertList = [Vector(k[0], k[1]) for k in posList]
		self.edgeList = [(posList[k], posList[k - 1]) for k in range(len(posList))]
		if closed:
			self.lineSegList = [LineSeg(posList[k], posList[k - 1]) for k in range(len(posList))]
		else:
			self.lineSegList = [LineSeg(posList[k], posList[k - 1]) for k in range(1, len(posList))]
