import sys
import random as rand

import numpy as np
import pygame as pg

import Physics.Vector as V

class Obj:
	def __init__(self, pos=(0, 0), color=(0, 0, 0)):
		self.pos = V.Vector(pos[0], pos[1])
		self.color = color
		self.geometry= None

	def setGeometryCircle(self,radius):
		self.Geometry = Circle(self.pos,radius)

	def setGeometryEllipse(self, r1=10, r2=10, res=20):
		self.geometry = Ellipse(self.pos, r1, r2, res)


class DynObj(Obj):
	def __init__(self, pos=(0, 0), vel=(0, 0), ambAcc=(0, -10), radius=10, mass=1, color=(0, 0, 0)):
		Obj.__init__(pos,color)
		self.vel = V.Vector(vel[0], vel[1])
		self.ambAcc = V.Vector(ambAcc[0], ambAcc[1])
		self.mass = mass


class StatObj(Obj):
	def __init__(self, pos=(0, 0), color=(0, 0, 0)):
		Obj.__init__(pos,color)

class Geometry:
	def __init__(self):
		pass

class Circle(Geometry):
	def __init__(self,pos ,radius):
		self.pos = pos
		self.radius =radius


class Circle1:
	def __init__(self, pos=(0, 0), vel=(0, 0), ambAcc=(0, -10), radius=10, mass=1, color=(0, 0, 0)):
		self.pos = V.Vector(pos[0], pos[1])
		self.vel = V.Vector(vel[0], vel[1])
		self.ambAcc = V.Vector(ambAcc[0], ambAcc[1])
		self.radius = radius
		self.mass = mass
		self.color = color


class Ellipse(Geometry):
	def __init__(self, pos=(0, 0), r1=10, r2=10, res=20):
		self.centre = V.Vector(pos[0], pos[1])
		self.radX = r1
		self.radY = r2
		self.res = res
		self.vertices = [(self.centre.x + self.radX * np.cos(theta), self.centre.y + self.radY * np.sin(theta)) for
		                 theta in np.linspace(0, 2 * np.pi, res + 1)[:-1]]
		print(np.linspace(0, 360, res + 1)[:-1])
		self.poly = Polygon(self.vertices)
		self.AABB = [V.Vector(self.centre.x - self.radX, self.centre.y - self.radY),
		             V.Vector(self.centre.x + self.radX, self.centre.y + self.radY)]


class MovPoly:
	def __init__(self,vertList,vel=(0,0),ambAcc= (0,0),mass=1,color = (0,0,0)):
		self.vertList= vertList
		self.pos = V.Vector(sum([k[0] for k in vertList])/len(vertList),
		                    sum([k[1] for k in vertList])/len(vertList))
		self.vel = V.Vector(vel[0],vel[1])
		self.ambAcc= V.Vector(ambAcc[0],ambAcc[1])
		self.mass = mass
		self.color = color
		self.poly= Polygon(vertList)
		self.AABB = [V.Vector(min([k[0] for k in vertList]),min([k[1] for k in vertList])),
					V.Vector(max([k[0] for k in vertList]),max([k[1] for k in vertList]))]


class ParaCurve:
	reference = {
		"cos": np.cos,
		"sin": np.sin,
		"tan": np.tan,
		"sec": lambda t: 1 / np.cos(t)
	}

	def __init__(self, pos=(0, 0), x_t='t', y_t='t', t_start=0, t_end=2 * np.pi, res=20, start=(0, 0), end=(1000, 600)):
		t: float
		self.centre = V.Vector(pos[0], pos[1])
		self.res = res
		self.x_t = eval(f"lambda t : {x_t}", ParaCurve.reference)
		self.y_t = eval(f"lambda t : {y_t}", ParaCurve.reference)
		self.vertices = [(self.centre.x + self.x_t(theta), self.centre.y + self.y_t(theta)) for
		                 theta in np.linspace(t_start, t_end, res + 1)]
		self.vertices_cut = []
		self.polyList = []
		self.createPolygon(start, end)
		# self.AABB =[V.Vector(start[0],start[1]),V.Vector(end[0],end[1])]

		# self.poly = Polygon(self.vertices,True)
		# print(self.vertices)
		minX = min([vertex[0] for vertList in self.vertices_cut for vertex in vertList])
		maxX = max([vertex[0] for vertList in self.vertices_cut for vertex in vertList])
		minY = min([vertex[1] for vertList in self.vertices_cut for vertex in vertList])
		maxY = max([vertex[1] for vertList in self.vertices_cut for vertex in vertList])
		self.AABB = [V.Vector(minX, minY), V.Vector(maxX, maxY)]

	def createPolygon(self, start=(), end=()):

		def isInside(vertex):
			return start[0] < vertex[0] < end[0] and start[1] < vertex[1] < end[1]

		def mapToEdge(vert1, vert2):
			if vert2[0] > end[0]:
				vert2 = end[0], vert1[1] + (vert2[1] - vert1[1]) * (end[0] - vert1[0]) / (vert2[0] - vert1[0])
			elif vert2[0] < start[0]:
				vert2 = start[0], vert1[1] + (vert2[1] - vert1[1]) * (start[0] - vert1[0]) / (vert2[0] - vert1[0])

			if vert2[1] > end[1]:
				vert2 = vert1[0] + (vert2[0] - vert1[0]) * (end[1] - vert1[1]) / (vert2[1] - vert1[1]), end[1]
			elif vert2[1] < start[1]:
				vert2 = vert1[0] + (vert2[0] - vert1[0]) * (start[1] - vert1[1]) / (vert2[1] - vert1[1]), start[1]
			return vert2

		polyIndex = -1
		newSet = True
		for vertIndex in range(len(self.vertices)):
			if isInside(self.vertices[vertIndex]):
				if newSet:
					self.vertices_cut.append([])
					polyIndex += 1
					self.vertices_cut[polyIndex].append(self.vertices[vertIndex])
					newSet = False
				else:
					self.vertices_cut[polyIndex].append(self.vertices[vertIndex])
			else:
				handled = False
				if vertIndex > 0:
					if isInside(self.vertices[vertIndex - 1]):
						v2 = mapToEdge(self.vertices[vertIndex - 1], self.vertices[vertIndex])
						self.vertices_cut[polyIndex].append(v2)
						handled = True
						newSet = True

				if vertIndex < len(self.vertices) - 1 and not handled:
					if isInside(self.vertices[vertIndex + 1]):
						if newSet:
							self.vertices_cut.append([])
							polyIndex += 1
							v2 = mapToEdge(self.vertices[vertIndex + 1], self.vertices[vertIndex])
							self.vertices_cut[polyIndex].append(v2)
							newSet = False
						else:
							v2 = mapToEdge(self.vertices[vertIndex + 1], self.vertices[vertIndex])
							self.vertices_cut[polyIndex].append(v2)

		# print(self.vertices_cut)
		# [print(vertex) for vertex in self.vertices]
		self.polyList = [Polygon(vertList, False) for vertList in self.vertices_cut]


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


class Polygon:
	def __init__(self, posList=[], closed=True):
		self.posList = posList
		self.vertList = [V.Vector(k[0], k[1]) for k in posList]
		self.edgeList = [(posList[k], posList[k - 1]) for k in range(len(posList))]
		if closed:
			self.lineSegList = [LineSeg(posList[k], posList[k - 1]) for k in range(len(posList))]
		else:
			self.lineSegList = [LineSeg(posList[k], posList[k - 1]) for k in range(1, len(posList))]


class Environ:
	def __init__(self):
		pg.init()

		self.WHITE = 255, 255, 255
		RED = 255, 0, 0
		GREEN = 0, 255, 0
		self.WIDTH = 600
		self.HEIGHT = 400
		self.ORIGIN = (0, self.HEIGHT)
		self.Display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
		self.n = 10
		self.dt = 1 / 200

		self.ambAcc = V.Vector(0, 0)
		self.circleList = []
		self.lineList = []
		self.lineSegList = []
		self.polyList = []
		self.ellipseList = []
		self.paraCurveList = []
		self.e = 1


		self.show()


	def show(self):
		RED = 255, 0, 0
		GREEN = 0, 255, 0



		self.Display.fill(self.WHITE)
		close = False

		self.circleList = [Circle1(pos=(rand.randint(0, self.WIDTH), rand.randint(0, self.HEIGHT)),
		                           vel=(rand.randint(-200, 200), rand.randint(-200, 200)), ambAcc=(0, 0), radius=10,
		                           mass=1, color=RED) for _ in range(self.n)]
		self.circleList.append(Circle1(pos=(720, 10), vel=(-100, 100), ambAcc=(0, 0), radius=10, mass=1, color=RED))
		self.circleList.append(Circle1(pos=(200, 200), vel=(-40, 120), ambAcc=(0, 0), radius=10, mass=1, color=GREEN))
		self.circleList.append(
			Circle1(pos=(300, 200), vel=(-40, -80), ambAcc=(0, 0), radius=10, mass=1, color=(0, 0, 255)))
		# self.lineList.append(Line(1,-2,30))
		# self.lineSegList.append(LineSeg((100, 0), (100, 200)))
		# self.polyList.append(Polygon([(50, 50), (50, 100), (200, 200), (100, 50)]))
		# self.ellipseList.append(Ellipse((200, 200), 20, 100, 80))
		self.paraCurveList.append(ParaCurve((100,100),"10*sec(t)","50*tan(t)",0,2*np.pi,80,end=(self.WIDTH,self.HEIGHT)))
		# self.paraCurveList.append(
		# 	ParaCurve((300, 200), "100*cos(t)", "50*sin(t)", 0, 2 * np.pi, 80, end=(self.WIDTH, self.HEIGHT)))


		clock = pg.time.Clock()
		self.temp_PolyList = []
		self.temp_Vert = []
		self.drawing = False

		while not close:
			clock.tick(int(1 / self.dt))
			mouse_pos = pg.mouse.get_pos()
			self.real_pos = (mouse_pos[0] + self.ORIGIN[0], self.ORIGIN[1] - mouse_pos[1])
			for event in pg.event.get():
				self.handleEvents(event)

			for particle in self.circleList:
				self.circleMove(particle)

			self.Render()
			# pg.draw.ellipse(self.Display, (0, 0, 0), (60, 30, 80, 140), 1)
			# [pg.draw.ellipse(self.Display,(0,0,255),(200+100*np.cos(t),200-10*np.sin(t),5,5)) for t in np.linspace(0,2*np.pi,40+1)[:-1]]
			pg.display.update()

	def handleEvents(self,event):
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
				self.polyList.append(Polygon(self.activeDraw,False))
				self.activeDraw = []
				self.drawing = False
			elif event.button == 2:
				self.activeDraw = []
				self.drawing = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				[print(poly.posList) for poly in self.polyList]

	def Render(self):
		self.Display.fill(self.WHITE)

		if self.drawing:
			if self.real_pos != self.activeDraw[-1]:
				self.temp_Vert = self.activeDraw + [self.real_pos]
				self.temp_Poly = Polygon(self.temp_Vert, False)
				self.drawPolygon(self.temp_Poly)
			if len(self.temp_Vert) > 1:
				self.drawPolygon(self.temp_Poly)
				self.temp_PolyList = [self.temp_Poly]
		# else:
		# 	self.temp_PolyList = []

		# else:
		# 	self.temp_PolyList =[]

		# self.draw(particle)
		self.drawCircles()
		self.drawLines()
		self.drawLineSegs()
		self.drawPolygons()
		self.drawEllipses()
		self.drawParaCurves()


	def circleMove(self, circle: Circle1):
		# newPos= V.Vector(10,10)
		newPos = V.Vector(circle.pos.x + circle.vel.x * self.dt + 1 / 2 * self.dt * self.dt * circle.ambAcc.x,
		                  circle.pos.y + circle.vel.y * self.dt + 1 / 2 * self.dt * self.dt * circle.ambAcc.y)
		newVel = V.Vector(circle.vel.x + self.dt * circle.ambAcc.x,
		                  circle.vel.y + self.dt * circle.ambAcc.y)
		collidingCircle = self.checkCollisionsCircle(circle, newPos)
		collidingLine = self.checkCollisionsLine(circle, newPos)
		collidingLineSeg, colTypeLS = self.checkCollisionsLineSeg(circle, newPos)
		collidingPoly, colTypeP, colSegP = self.checkCollisionsPoly(circle, newPos)
		collidingEllipse, colTypeE, colSegE = self.checkCollisionsEllipse(circle, newPos)
		collidingParaCurve, colTypePC, colSegPC = self.checkCollisionsParaCurve(circle, newPos)
		# print(newVel)

		if newPos.x < circle.radius and circle.vel.x < 0:
			circle.vel.x *= -1
		elif newPos.x > self.WIDTH - circle.radius and circle.vel.x > 0:
			circle.vel.x *= -1
		elif newPos.y > self.HEIGHT - circle.radius and circle.vel.y > 0:
			circle.vel.y *= -1
		elif newPos.y < circle.radius and circle.vel.y < 0:
			circle.vel.y *= -1

		elif collidingLine != None:
			self.collideLine(circle, collidingLine, newPos, newVel)
		elif collidingLineSeg != None:
			self.collideLineSeg(circle, collidingLineSeg, colTypeLS, newPos, newVel)
		elif collidingPoly != None:
			self.collidePoly(circle, collidingPoly, colTypeP, colSegP, newPos, newVel)
		elif collidingCircle != None:
			self.collideCircle(circle, collidingCircle, newPos, newVel)
		elif collidingEllipse != None:
			self.collideEllipse(circle, collidingEllipse, colTypeE, colSegE, newPos, newVel)
		elif collidingParaCurve != None:
			self.collideParaCurve(circle, collidingParaCurve, colTypePC, colSegPC, newPos, newVel)

		else:
			circle.pos = newPos
			circle.vel = newVel
		# particle.rotation += particle.angVel

	def drawCircle(self,pos:V.Vector,radius,color):
		pg.draw.ellipse(self.Display, color, (
			pos.x + self.ORIGIN[0] - radius, self.ORIGIN[1] - pos.y - radius,
			2 * radius, 2 * radius))

	def drawCircles(self):
		for circle in self.circleList:
			self.drawCircle(circle.pos,circle.radius,circle.color)

		# pg.draw.line(self.Display, (0, 0, 0), (particle.pos.x + self.ORIGIN[0], self.ORIGIN[1] - particle.pos.y),
		#              (particle.pos.x + particle.radius * np.cos(particle.rotation * np.pi / 180) + self.ORIGIN[0],
		#               self.ORIGIN[1] - particle.pos.y - particle.radius * np.sin(particle.rotation * np.pi / 180)))

	def drawLines(self):
		for line in self.lineList:
			pg.draw.line(self.Display, (0, 0, 0), (-line.c / line.a + self.ORIGIN[0], self.ORIGIN[1] - 0),
			             (-(self.HEIGHT * line.b + line.c) / line.a + self.ORIGIN[0], self.ORIGIN[1] - self.HEIGHT))

	def drawLineSeg(self, lineSeg: LineSeg):
		# print((int(lineSeg.pos1.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos1.y)))
		pg.draw.line(self.Display,
		             (0, 0, 0), (int(lineSeg.pos0.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos0.y)),
		             (int(lineSeg.pos1.x + self.ORIGIN[0]), int(self.ORIGIN[1] - lineSeg.pos1.y)))

	def drawLineSegs(self):
		for lineSeg in self.lineSegList:
			self.drawLineSeg(lineSeg)

	def drawPolygons(self):
		for poly in self.polyList:
			for lineSeg in poly.lineSegList:
				self.drawLineSeg(lineSeg)

	def drawPolygon(self, poly):
		for lineSeg in poly.lineSegList:
			self.drawLineSeg(lineSeg)

	def drawEllipses(self):
		for ellipse in self.ellipseList:
			self.drawPolygon(ellipse.poly)
		# pg.draw.rect(self.Display,(0,0,0),(ellipse.AABB[0].x,self.ORIGIN[1]-ellipse.AABB[1].y,ellipse.AABB[1].x-ellipse.AABB[0].x,ellipse.AABB[1].y-ellipse.AABB[0].y),1)

	def drawParaCurves(self):
		for paraCurve in self.paraCurveList:
			for poly in paraCurve.polyList:
				self.drawPolygon(poly)
			# for vertList in paraCurve.vertices_cut[:]:
			# 	for vert in vertList[:]:
			##print(vertList)
			# pg.draw.ellipse(self.Display,(0,0,255),(vert[0],self.ORIGIN[1]-vert[1],2,2))
			# for vert in paraCurve.vertices:
			# 	x = vert if -10**5<vert[0]<10**5 else (10**4,10**4)
			# 	pg.draw.ellipse(self.Display, (0, 0, 255), (x[0], self.ORIGIN[1] - x[1], 2, 2))
			pg.draw.rect(self.Display, (0, 0, 0), (
			paraCurve.AABB[0].x, self.ORIGIN[1] - paraCurve.AABB[1].y, paraCurve.AABB[1].x - paraCurve.AABB[0].x,
			paraCurve.AABB[1].y - paraCurve.AABB[0].y), 1)

	def collideLine(self, particle, collidingLine, newPos, newVel):
		if collidingLine.b == 0:
			axis_norm = V.Vector(0, 1)
		else:
			axis = V.Vector(1, -collidingLine.a / collidingLine.b)
			axis_norm = V.v_Unit(axis)
		# abs(line.a * particle.pos.x + line.b * particle.pos.y + line.c) / (line.a**2 + line.b**2)**(.5)
		dist_original = abs(
			collidingLine.a * particle.pos.x + collidingLine.b * particle.pos.y + collidingLine.c) / (
				                (collidingLine.a**2 + collidingLine.b**2)**(.5))
		dist_new = abs(collidingLine.a * newPos.x + collidingLine.b * newPos.y + collidingLine.c) / (
				(collidingLine.a**2 + collidingLine.b**2)**(.5))

		if dist_original > dist_new:
			u_aax, u_pax = V.v_Resolve(particle.vel, axis_norm)
			particle.vel = V.v_Add(u_aax, V.v_sMul(u_pax, -1))

		else:
			particle.pos = newPos

	def collideLineSeg(self, particle, collidingLineSeg, colTypeLS, newPos, newVel):
		if colTypeLS == 0:
			self.collideLine(particle, collidingLineSeg, newPos, newVel)

		elif colTypeLS == 1:
			# print('type 1')
			vert0 = V.v_Sub(collidingLineSeg.pos0, particle.pos)
			vert1 = V.v_Sub(collidingLineSeg.pos1, particle.pos)
			vert0_new = V.v_Sub(collidingLineSeg.pos0, newPos)
			vert1_new = V.v_Sub(collidingLineSeg.pos1, newPos)

			minVert_new = vert0_new if vert0_new.mag < vert1_new.mag else vert1_new
			minVert = vert0 if vert0.mag < vert1.mag else vert1

			if minVert_new.y == 0:
				axis_norm = V.Vector(0, 1)
			else:
				axis_norm = V.v_Unit(minVert_new)

			if minVert.mag > minVert_new.mag:
				u_aax, u_pax = V.v_Resolve(particle.vel, axis_norm)
				particle.vel = V.v_Add(V.v_sMul(u_aax, -1), u_pax)
				particle.pos = newPos
			else:
				particle.pos = newPos

	def collidePoly(self, particle, collidingPoly, colTypeP, colSegP, newPos, newVel):
		self.collideLineSeg(particle, colSegP, colTypeP, newPos, newVel)

	def collideCircle(self, particle, collidingCircle, newPos, newVel):
		axis = V.v_Sub(collidingCircle.pos, newPos)
		axis_norm = V.v_Unit(axis)
		u1_aax, u1_pax = V.v_Resolve(newVel, axis)
		u2_aax, u2_pax = V.v_Resolve(collidingCircle.vel, axis)
		m1 = particle.mass
		m2 = collidingCircle.mass
		e = self.e

		u1 = V.v_dMul(u1_aax, axis_norm)
		u2 = V.v_dMul(u2_aax, axis_norm)
		if u1 > u2:
			v1_aax_m = u1 * (m1 - e * m2) / (m1 + m2) + u2 * (m2 + e * m2) / (m1 + m2)
			v2_aax_m = u1 * (m1 + e * m1) / (m1 + m2) + u2 * (m2 - e * m1) / (m1 + m2)

			v1_aax = V.toVector(v1_aax_m, axis.dir)
			v2_aax = V.toVector(v2_aax_m, axis.dir)

			v1 = V.v_Add(v1_aax, u1_pax)
			v2 = V.v_Add(v2_aax, u2_pax)

			particle.vel = v1
			# particle.pos = newPos
			collidingCircle.vel = v2
			if  V.v_dMul(v2,V.v_Sub(v2,v1))>0:
				# print("assertion failed")
				pass
		else:
			particle.pos = newPos
			particle.vel = newVel


	def collideEllipse(self, particle, collidingEllipse, colTypeE, colSegE, newPos, newVel):
		self.collidePoly(particle, collidingEllipse.poly, colTypeE, colSegE, newPos, newVel)

	def collideParaCurve(self, particle, collidingParaCurve, colTypePC, colSegPC, newPos, newVel):
		self.collideLineSeg(particle, colSegPC, colTypePC, newPos, newVel)

	def checkCollisionsCircle(self, particle: Circle1, newPos: V.Vector):
		remCircles = [k for k in self.circleList if
		              abs(k.pos.x - particle.pos.x) > 10**-2 or abs(k.pos.y - particle.pos.y) > 10**-2]
		for circle in remCircles:
			collision = (circle.pos.x - newPos.x)**2 + (circle.pos.y - newPos.y)**2 < (
					particle.radius + circle.radius)**2
			if collision:
				collidingParticle = circle
				return collidingParticle
		return None

	def checkCollisionsLine(self, particle: Circle1, newPos: V.Vector):
		for line in self.lineList:
			dist = abs(line.a * newPos.x + line.b * newPos.y + line.c) / (line.a**2 + line.b**2)**(.5)
			if dist < particle.radius:
				return line
		return None

	def checkLineSeg(self, particle, lineSeg, newPos):
		dist = abs(lineSeg.a * newPos.x + lineSeg.b * newPos.y + lineSeg.c) / (lineSeg.a**2 + lineSeg.b**2)**(.5)
		if dist < particle.radius:
			if lineSeg.b == 0:
				axis_norm = V.Vector(0, 1)
			else:
				axis = V.Vector(1, -lineSeg.a / lineSeg.b)
				axis_norm = V.v_Unit(axis)
			vert0 = V.v_Sub(lineSeg.pos0, newPos)
			vert1 = V.v_Sub(lineSeg.pos1, newPos)
			dir0 = V.v_dMul(axis_norm, vert0)
			dir1 = V.v_dMul(axis_norm, vert1)
			if dir0 * dir1 <= 0:
				return lineSeg, 0
			else:
				minDist = min(vert0.mag, vert1.mag)
				if minDist < particle.radius:
					return lineSeg, 1

		return None, 0

	def checkCollisionsLineSeg(self, particle: Circle1, newPos: V.Vector):
		for lineSeg in self.lineSegList:
			collidingSeg, colType = self.checkLineSeg(particle, lineSeg, newPos)
			if collidingSeg != None:
				return collidingSeg, colType
		return None, 0

	def checkPoly(self, poly, particle, newPos):
		colList = []
		for lineSeg in poly.lineSegList:
			collidingParticle, coltype = self.checkLineSeg(particle, lineSeg, newPos)
			if collidingParticle != None:
				if coltype == 0:
					return poly, 0, lineSeg
				if coltype == 1:
					colList.append(lineSeg)
		if len(colList) > 0:
			return poly, 1, colList[0]

		return None, 0, 0

	def checkCollisionsPoly(self, particle: Circle1, newPos: V.Vector):
		for poly in self.polyList + self.temp_PolyList:
			colPoly, colType, ColSeg = self.checkPoly(poly, particle, newPos)
			if colPoly != None:
				return colPoly, colType, ColSeg
		return None, 0, 0

	def checkCollisionsEllipse(self, particle: Circle1, newPos: V.Vector):
		for ellipse in self.ellipseList:
			# print(max_rad)
			if self.check_circle_AABB_collision(particle, newPos, ellipse.AABB):
				colEllipse, colType, colSeg = self.checkPoly(ellipse.poly, particle, newPos)
				if colEllipse != None:
					return ellipse, colType, colSeg
		return None, 0, 0

	def checkCollisionsParaCurve(self, particle, newPos):
		for paraCurve in self.paraCurveList:
			if self.check_circle_AABB_collision(particle, newPos, paraCurve.AABB):
				for poly in paraCurve.polyList:
					colParaCurve, colType, colSeg = self.checkPoly(poly, particle, newPos)
					if colParaCurve != None:
						return colParaCurve, colType, colSeg
		return None, 0, 0

	def check_circle_AABB_collision(self, particle:Circle1, newPos, AABB):
		return np.sign(AABB[0].x - (newPos.x + particle.radius)) \
		       * np.sign(newPos.x - particle.radius - AABB[1].x) >= 0 \
		       and np.sign(AABB[0].y - (newPos.y + particle.radius)) \
		       * np.sign(newPos.y - particle.radius - AABB[1].y) >= 0

	def check_point_AABB_collision(self,point:tuple,AABB:V.Vector):
		return np.sign(AABB[0].x - point[0]) \
		       * np.sign(point[0] - AABB[1].x) >= 0 \
		       and np.sign(AABB[0].y - point[1]) \
		       * np.sign(point[1] - AABB[1].y) >= 0

	def check_movPoly_movPoly(self,poly1:MovPoly,poly2:MovPoly,newPos:V.Vector):
		p1_vertices = [(k[0]+ newPos.x,k[1]+newPos.y) for k in poly1.vertList]
		p1_AABB_vert = [vert for vert in p1_vertices if self.check_point_AABB_collision(vert,poly2.AABB)]
		if len(p1_AABB_vert) ==0 :
			return None

		p1_inter_vert=[]

		for vert1 in p1_AABB_vert:
			x,y = vert1
			hitCount = 0
			for edge in poly2.poly.edgeList:
				vert2,vert3 = edge
				x1,y1 = vert2
				x2,y2 = vert3

				Q = (y-y1)/(y2-y1)
				if not 0<=Q<1:
					continue
				P = (x1-x)+(x2-x1)*Q
				if P<0:
					continue
				hitCount +=1

			if hitCount%2 ==1:
				p1_inter_vert.append((vert1,edge))

		if len(p1_inter_vert)>0:
			return p1_inter_vert

		return None

	def ray_poly_Distance(self,origin:V.Vector,angle,poly:Polygon):
		distance = 10**5
		for lineSeg in poly.lineSegList:
			signX = np.cos(angle)
			signY = np.sin(angle)
			c = lineSeg.pos0
			d =lineSeg.pos1
			a = origin
			if not((c.x-a.x)*signX>0 and (c.y-a.y)*signY>0 or(d.x-a.x)*signX>0 and (d.y-a.y)*signY>0 ):
				continue
			b= a+ V.toVector(1,angle)

			r = b-a
			s = d-c

			t = ((c-a)@s).z/(r@s).z
			u = ((a-c)@r).z/(s@r).z
			if t>=0 and 0<=u<=1:
				p = a+(t*r)
				dist = (p-a).mag
				distance= min(dist,distance)
		return distance








if __name__ == '__main__':
	import time
	env = Environ()
	poly = Polygon([(86, 87), (216, 84), (299, 86), (425, 111), (440, 128), (479, 199), (479, 234), (476, 284), (444, 350),
			 (387, 366), (314, 370), (262, 370), (214, 370), (149, 372), (123, 375), (88, 344), (96, 326), (106, 311),
			 (143, 308), (183, 308), (199, 311), (233, 312), (274, 314), (316, 317), (389, 319), (406, 298), (411, 268),
			 (411, 248), (408, 228), (406, 205), (402, 188), (389, 167), (387, 163), (352, 146), (315, 138), (294, 138),
			 (253, 140), (223, 140), (197, 140), (172, 139), (142, 138), (114, 137), (92, 137)],False)
	time0 = time.perf_counter()
	env.ray_poly_Distance(V.Vector(10,200),np.pi*3.4,poly)
	print(time.perf_counter()-time0)
	# env.show()
