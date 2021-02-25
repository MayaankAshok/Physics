import pygame as pg
from Physics.Vector import *
from Physics.Main.Geometry import *
from Physics.Main.BaseGeometry import *
from Physics.Main.Objects import *
import sys


class Screen:
	def __init__(self):
		pg.init()
		self.WHITE = 255, 255, 255
		self.RED = 255, 0, 0
		self.GREEN = 0, 255, 0
		self.WIDTH = 600
		self.HEIGHT = 400
		self.ORIGIN = (0, self.HEIGHT)
		self.Display = pg.display.set_mode((self.WIDTH, self.HEIGHT))

	def fill(self):
		self.Display.fill(self.WHITE)

	def getPos(self):
		return pg.mouse.get_pos()

	def drawObject(self,obj :Obj):
		if obj.geometry.type == 'circle':
			self.drawCircle(obj)

		if obj.geometry.type == 'ellipse':
			self.drawEllipse


	def drawCircle(self,obj:Obj):
		pg.draw.ellipse(self.Display, obj.color, (
			obj.pos.x + self.ORIGIN[0] - obj.geometry.radius, self.ORIGIN[1] - obj.pos.y - obj.geometry.radius,
			2 * obj.geometry.radius, 2 * obj.geometry.radius))

	def drawPolygon(self, obj:Obj):
		for lineSeg in obj.geometry.lineSegList:
			self.drawLineSeg(lineSeg)

	def drawLineSeg(self, lineSeg: LineSeg):
		# print((int(lineSeg.pos1.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos1.y)))
		pg.draw.line(self.Display,
		             (0, 0, 0), (int(lineSeg.pos0.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos0.y)),
		             (int(lineSeg.pos1.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos1.y)))

	def drawEllipse(self,obj:Obj):
		self.drawPolygon(obj.geometry.poly)

class SpaceState:
	def __init__(self):
		self.circleList = []
		self.lineList = []
		self.lineSegList = []
		self.polyList = []
		self.ellipseList = []
		self.paraCurveList = []


class Space:
	def __init__(self):

		self.n = 10

		self.dt = 1 / 200
		self.ambAcc = Vector(0, -10)
		self.e = 1.1

		self.spaceState = SpaceState()
		self.screen = Screen()

		self.addObjects()
		self.show()

	def addObjects(self):

		ball = DynObj(pos=(100, 100), vel=(10, 10), ambAcc=(self.ambAcc.x,self.ambAcc.y), mass=10, color=(100, 100, 255))
		ball.setGeometryCircle(10)
		# self.spaceState.circleList.append(ball)

	# self.circleList = [Circle(pos=(rand.randint(0, self.WIDTH), rand.randint(0, self.HEIGHT)),
	#                           vel=(rand.randint(-200, 200), rand.randint(-200, 200)), ambAcc=(0, -100), radius=10,
	#                           mass=1, color=RED) for _ in range(self.n)]
	# self.circleList.append(Circle(pos = (720,10) , vel = (-100,100) , ambAcc=(0,0), radius=10, mass=1,color=RED))
	# self.circleList.append(Circle(pos = (200,200) , vel = (-40,120) , ambAcc=(0,0), radius=10, mass=1,color=GREEN))
	# self.circleList.append(Circle(pos = (300,200) , vel = (-40,-80) , ambAcc=(0,0), radius=10, mass=1,color=(0,0,255)))
	# self.lineList.append(Line(1,-2,30))
	# self.lineSegList.append(LineSeg((100, 0), (100, 200)))
	# self.polyList.append(Polygon([(50, 50), (50, 100), (200, 200), (100, 50)]))
	# self.ellipseList.append(Ellipse((200, 200), 20, 100, 80))
	# self.paraCurveList.append(ParaCurve((400,200),"100*cos(t)","50*sin(t)",0,2*np.pi,80,end=(self.WIDTH,self.HEIGHT)))
	# self.paraCurveList.append(
	# 	ParaCurve((300, 200), "100*cos(t)", "50*sin(t)", 0, 2 * np.pi, 80, end=(self.WIDTH, self.HEIGHT)))

	def show(self):
		ORIGIN = self.screen.ORIGIN

		self.screen.fill()
		close = False

		clock = pg.time.Clock()
		self.temp_PolyList = []
		self.temp_Vert = []
		self.drawing = False

		while not close:
			clock.tick(int(1 / self.dt))
			mouse_pos = self.screen.getPos()
			self.real_pos = (mouse_pos[0] + ORIGIN[0], ORIGIN[1] - mouse_pos[1])
			for event in pg.event.get():
				# self.handleEvents(event)
				pass

			# for particle in self.circleList:
			# 	self.circleMove(particle)

			# self.Render()
			pg.display.update()

if __name__ == '__main__':
	space = Space()