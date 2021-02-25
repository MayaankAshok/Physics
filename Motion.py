import time
import sys
import pygame as pg
import Vector as V

pg.init()
start_time = time.time()


class Particle:
	def __init__(self, pos=[0, 0], vel=[0, 0], acc=[0, 0], m=1):
		self.pos = pos
		self.vel = V.Vector(vel[0], vel[1])

		self.acc = V.Vector(acc[0], acc[1])
		self.force = V.Vector(0, 0)
		self.mass = m

	def setAcc(self):
		self.acc.x = self.acc.x+ self.force.x / self.mass  # F = ma
		self.acc.y = self.acc.y+self.force.y / self.mass

	def setVel(self, dt):
		self.vel.x = self.vel.x + self.acc.x * dt  # v = u + at
		self.vel.y = self.vel.y + self.acc.y * dt

	def setPos(self, dt):
		self.pos = [self.pos[0] + self.vel.x * dt + self.acc.x * (dt**2) * 0.5,  # s = ut + 1/2 a t^2
		            self.pos[1] + self.vel.y * dt + self.acc.y * (dt**2) * 0.5]




class Setup():

	def __init__(self, pList: [Particle], tInterval=10**(0),tmax= 10):
		self.plist = pList
		self.dt = tInterval
		self.times = []
		self.tmax = tmax
		self.imgL = []
		self.rectL = []
		self.data = {
			'pos': {},
			'vel': {},
			'acc': {}
		}

		self.particleList = []
		for index, n in enumerate(self.plist):
			self.particleList.append(Particle(n[0], n[1], n[2], n[3]))
			self.data['pos'][index] = {
				'x': [],
				'y': []
			}
			self.data['vel'][index] = {
				'x': [],
				'y': []
			}
			self.data['acc'][index] = {
				'x': [],
				'y': []
			}

		self.setupMotion()

	def setForce(self):
		const = 1
		for particle in self.particleList:
			fx = 0
			fy = 0
			remPrts = self.particleList.copy()
			remPrts.remove(particle)
			for remPrt in remPrts:
				if not (abs(particle.pos[1] - remPrt.pos[1]) < 1 and abs(particle.pos[0] - remPrt.pos[0]) < 1):
					# both particles dont have same x or y coordinate
					dist = ((particle.pos[1] - remPrt.pos[1])**2 + (particle.pos[0] - remPrt.pos[0])**2)
					if dist < 10000: dist = 10000
					magn = const * (particle.mass * remPrt.mass) / dist
					dir_vec = V.Vector(remPrt.pos[0] - particle.pos[0], remPrt.pos[1] - particle.pos[1])
					vect = V.toVector(magn, dir_vec.dir)
					fx += vect.x
					fy += vect.y

			particle.force.x = fx
			particle.force.y = fy
			V.Vupdate(particle.force)

	def setupMotion(self):
		self.t = 0

		while self.t < self.tmax:

			self.times.append(self.t)
			self.setForce()

			for index, particle in enumerate(self.particleList):
				particle.setAcc()
				particle.setVel(self.dt)
				particle.setPos(self.dt)
				self.data['pos'][index]['x'].append(particle.pos[0])
				self.data['pos'][index]['y'].append(particle.pos[1])
			# self.data['vel'][index]['x'].append(particle.vel.x)
			# self.data['vel'][index]['y'].append(particle.vel.y)
			# self.data['acc'][index]['x'].append(particle.acc.x)
			# self.data['acc'][index]['y'].append(particle.acc.y)
			self.t += self.dt


WHITE = 255,255,255
BLACK = 0,0,0
RED  =255,0,0
BLUE = 0,0,255

Display = pg.display.set_mode((1080,1000))
Display.fill(WHITE)

List = [[[100, 100], [0, 0], [0, 0], 25_000_000],
        [[500, 100], [0, 250], [0, 0], 1_000_000]]
dt =.1
s = Setup(List,dt,40)
data = s.data
particlesNum = len(s.particleList)
# print(data)
fps = int(1/dt)

print(len(data['pos'][0]['x']))
clock = pg.time.Clock()
t= 0
while t< len(data['pos'][0]['x']):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
			# break
	clock.tick(fps)
	Display.fill(WHITE)
	for n in range(2):
		# print(n, )
		pg.draw.rect(Display,(RED,BLUE)[n],(data['pos'][n]['x'][t], data['pos'][n]['y'][t], 10, 10))
		# print(data['pos'][n]['x'][d], d)
	t+=1
	pg.display.update()

# print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	pass
'''
p1 = Particle([-1,0], [0, 0], [0, 0],  4)
p2 = Particle([1,0], [0, 0], [0, 0],  4)
p3 = Particle([3,0], [0, 0], [0, 0],  4)
plist = [p1, p2,p3]
setForce(plist)

print(p3.force.x)

'''
'''
# print("--- %s seconds ---" % (time.time() - start_time))
'''
