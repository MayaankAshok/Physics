import pygame as pg
from Main.Vector import *
from Main.BaseGeometry import *
from Main.Geometry import *
from Main.Objects import *
from typing import List
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

	def drawObject(self, obj: Obj):
		if obj.geometry.type == 'circle':
			self.drawCircle(obj)

		if obj.geometry.type == 'ellipse':
			self.drawEllipse

	def drawCircle(self, obj: Obj):
		pg.draw.ellipse(self.Display, obj.color, (
			obj.pos.x + self.ORIGIN[0] - obj.geometry.radius, self.ORIGIN[1] - obj.pos.y - obj.geometry.radius,
			2 * obj.geometry.radius, 2 * obj.geometry.radius))

	def drawPolygon(self, obj: Obj):
		for lineSeg in obj.geometry.lineSegList:
			self.drawLineSeg(lineSeg)

	def drawLineSeg(self, lineSeg: LineSeg):
		# print((int(lineSeg.pos1.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos1.y)))
		pg.draw.line(self.Display,
					 (0, 0, 0), (int(lineSeg.pos0.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos0.y)),
					 (int(lineSeg.pos1.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos1.y)))

	def drawEllipse(self, obj: Obj):
		self.drawPolygon(obj.geometry.poly)


class SpaceState:
	def __init__(self):
		self.dynObjList = []
		self.statObjList = []


class CollisionHandler:
	@staticmethod
	def circle(circle: Ball, dynObjList: List[DynObj], statObjList: List[StatObj], dt: float,WIDTH,HEIGHT,e):

		newPos = Vector(circle.pos.x + circle.vel.x * dt + 1 / 2 * dt * dt * circle.ambAcc.x,
						circle.pos.y + circle.vel.y * dt + 1 / 2 * dt * dt * circle.ambAcc.y)
		newVel = Vector(circle.vel.x + dt * circle.ambAcc.x,
						circle.vel.y + dt * circle.ambAcc.y)

		if newPos.x < circle.geometry.radius and circle.vel.x < 0:
			circle.vel.x *= -1
			return
		elif newPos.x > WIDTH - circle.geometry.radius and circle.vel.x > 0:
			circle.vel.x *= -1
			return
		elif newPos.y > HEIGHT - circle.geometry.radius and circle.vel.y > 0:
			circle.vel.y *= -1
			return
		elif newPos.y < circle.geometry.radius and circle.vel.y < 0:
			circle.vel.y *= -1
			return

		for dynObj in dynObjList:
			if dynObj== circle:
				# print("whoops")
				continue
			elif dynObj.geometry.type == "circle":
				if CollisionChecker.circle_circle(circle, newPos, dynObj):
					# print('collided',circle==dynObj)
					Collider.circle_circle(circle, newPos, newVel, dynObj,e)
					return
		circle.pos = newPos
		circle.vel = newVel



class CollisionChecker:
	@staticmethod
	def circle_circle(circle1: Ball, newPos: Vector, circle2: Ball):
		return circle1.geometry.radius ** 2 + circle2.geometry.radius ** 2 > (newPos - circle2.pos).getMagnSquared()


class Collider:
	@staticmethod
	def circle_circle(circle1: Ball, newPos: Vector, newVel: Vector, circle2: Ball,e):
		axis =v_Sub(circle2.pos, newPos)
		axis_norm = v_Unit(axis)
		u1_aax, u1_pax = v_Resolve(newVel, axis)
		u2_aax, u2_pax = v_Resolve(circle2.vel, axis)
		m1 = circle1.mass
		m2 = circle2.mass
		# e = self.e

		u1 = v_dMul(u1_aax, axis_norm)
		u2 = v_dMul(u2_aax, axis_norm)
		if u1 > u2:
			v1_aax_m = u1 * (m1 - e * m2) / (m1 + m2) + u2 * (m2 + e * m2) / (m1 + m2)
			v2_aax_m = u1 * (m1 + e * m1) / (m1 + m2) + u2 * (m2 - e * m1) / (m1 + m2)

			v1_aax = toVector(v1_aax_m, axis.dir)
			v2_aax = toVector(v2_aax_m, axis.dir)

			v1 = v_Add(v1_aax, u1_pax)
			v2 = v_Add(v2_aax, u2_pax)

			circle1.vel = v1
			# particle.pos = newPos
			circle2.vel = v2
			if v_dMul(v2, v_Sub(v2, v1)) > 0:
				# raise Exception("failed")
				pass
		else:
			circle1.pos = newPos
			circle1.vel = newVel


class Space:
	def __init__(self):

		self.n = 10

		self.dt = 1 / 200
		self.ambAcc = Vector(0, 0)
		self.e = 1

		self.spaceState = SpaceState()
		self.screen = Screen()

		self.temp_PolyList = []
		self.temp_Vert = []
		self.drawing = False

		self.addObjects()
		self.show()

	def addObjects(self):

		ball = Ball(pos=(100,105),vel = (100,0),ambAcc=(0,0),radius =10,color=(255,0,0))
		ball2 = Ball(pos=(200,100),vel = (-100,0),ambAcc=(0,0),radius =10,color=(0,255,0))

		self.spaceState.dynObjList.append(ball)
		self.spaceState.dynObjList.append(ball2)

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

		while not close:
			self.screen.fill()

			clock.tick(int(1 / self.dt))
			mouse_pos = self.screen.getPos()
			self.real_pos = (mouse_pos[0] + ORIGIN[0], ORIGIN[1] - mouse_pos[1])
			for event in pg.event.get():
				self.handleEvents(event)

			for body in self.spaceState.dynObjList:
				# print(body.pos)
				self.dynObjMove(body)

			for body in self.spaceState.dynObjList+self.spaceState.statObjList:
				self.screen.drawObject(body)

			pg.display.update()

	def handleEvents(self, event):
		if event.type == pg.QUIT:
			sys.exit()
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1 and self.drawing == False:
				self.activeDraw = [self.real_pos]
				self.drawing = True
			elif event.button == 1 and self.drawing:
				self.activeDraw.append(self.real_pos)
			elif event.button == 3 and self.drawing:
				self.activeDraw.append(self.real_pos)
				self.polyList.append(Polygon(self.activeDraw, False))
				self.activeDraw = []
				self.drawing = False
			elif event.button == 2:
				self.activeDraw = []
				self.drawing = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				[print(poly.posList) for poly in self.polyList]

	def dynObjMove(self, dynObj: DynObj):
		if dynObj.geometry.type == "circle":
			CollisionHandler.circle(dynObj, self.spaceState.dynObjList, self.spaceState.statObjList, self.dt,
									self.screen.WIDTH,self.screen.HEIGHT,self.e)



# collidingCircle = self.checkCollisionsCircle(circle, newPos)
# collidingLine = self.checkCollisionsLine(circle, newPos)
# collidingLineSeg, colTypeLS = self.checkCollisionsLineSeg(circle, newPos)
# collidingPoly, colTypeP, colSegP = self.checkCollisionsPoly(circle, newPos)
# collidingEllipse, colTypeE, colSegE = self.checkCollisionsEllipse(circle, newPos)
# collidingParaCurve, colTypePC, colSegPC = self.checkCollisionsParaCurve(circle, newPos)
# print(newVel)

# if newPos.x < circle.radius and circle.vel.x < 0:
# 	circle.vel.x *= -1
# elif newPos.x > self.WIDTH - circle.radius and circle.vel.x > 0:
# 	circle.vel.x *= -1
# elif newPos.y > self.HEIGHT - circle.radius and circle.vel.y > 0:
# 	circle.vel.y *= -1
# elif newPos.y < circle.radius and circle.vel.y < 0:
# 	circle.vel.y *= -1

# elif collidingLine != None:
# 	self.collideLine(circle, collidingLine, newPos, newVel)
# elif collidingLineSeg != None:
# 	self.collideLineSeg(circle, collidingLineSeg, colTypeLS, newPos, newVel)
# elif collidingPoly != None:
# 	self.collidePoly(circle, collidingPoly, colTypeP, colSegP, newPos, newVel)
# elif collidingCircle != None:
# 	self.collideCircle(circle, collidingCircle, newPos, newVel)
# elif collidingEllipse != None:
# 	self.collideEllipse(circle, collidingEllipse, colTypeE, colSegE, newPos, newVel)
# elif collidingParaCurve != None:
# 	self.collideParaCurve(circle, collidingParaCurve, colTypePC, colSegPC, newPos, newVel)

# else:
# 	circle.pos = newPos
# 	circle.vel = newVel


if __name__ == '__main__':
	space = Space()
