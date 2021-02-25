
import Physics.Vector as V

class Obj:
	def __init__(self, pos=(0, 0), color=(0, 0, 0)):
		self.pos = V.Vector(pos[0], pos[1])
		self.color = color
		self.geometry= None

	def setGeometryCircle(self,radius):
		self.geometry = Circle(self.pos,radius)


	def setGeometryEllipse(self, r1=10, r2=10, res=20):
		self.geometry = Ellipse(self.pos, r1, r2, res)

class DynObj(Obj):
	def __init__(self, pos=(0, 0), vel=(0, 0), ambAcc=(0, -10), mass=1, color=(0, 0, 0)):
		Obj.__init__(self,pos,color)
		self.vel = V.Vector(vel[0], vel[1])
		self.ambAcc = V.Vector(ambAcc[0], ambAcc[1])
		self.mass = mass

class Geometry:
	def __init__(self):
		pass

class Circle(Geometry):
	def __init__(self,pos ,radius):
		self.pos = pos
		self.radius =radius

class Ball(DynObj):
	def __init__(self, pos=(0, 0), vel=(0, 0), ambAcc=(0, -10), radius=10, mass=1, color=(0, 0, 0)):
		DynObj.__init__(self,pos,vel,ambAcc,mass,color)
		Obj.setGeometryCircle(self,radius)


ball= Ball()
print(ball.geometry
      )