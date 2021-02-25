import numpy as np
from Physics.Vector import *
from .Geometry import *


class Obj:
	def __init__(self, pos=(0, 0), color=(0, 0, 0)):
		self.pos = Vector(pos[0], pos[1])
		self.color = color
		self.geometry = None

	def setGeometryCircle(self, radius):
		self.geometry = Circle(self.pos, radius)

	def setGeometryEllipse(self, r1=10, r2=10, res=20):
		self.geometry = Ellipse(self.pos, r1, r2, res)


class DynObj(Obj):
	def __init__(self, pos=(0, 0), vel=(0, 0), ambAcc=(0, -10), mass=1, color=(0, 0, 0)):
		Obj.__init__(self,pos, color)
		self.vel = Vector(vel[0], vel[1])
		self.ambAcc = Vector(ambAcc[0], ambAcc[1])
		self.mass = mass

class Ball(DynObj):

class StatObj(Obj):
	def __init__(self, pos=(0, 0), color=(0, 0, 0)):
		Obj.__init__(self,pos, color)
