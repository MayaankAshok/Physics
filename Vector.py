import numpy as np


class Vector:

	def __init__(self, x=int, y=int, z=0):
		import numpy as np
		self.x = x
		self.y = y
		self.z = z
		self.mag = np.sqrt(self.x**2 + self.y**2 + self.z**2)

		if self.x != 0:
			if self.y != 0:
				# if x>0 and y>0:
				self.dir = np.arctan(self.y / self.x) * (180 / np.pi)
				if x < 0:
					self.dir = 180 + np.arctan(self.y / self.x) * (180 / np.pi)

			else:
				if self.x > 0:
					self.dir = 0
				elif self.x < 0:
					self.dir = 180
		else:
			if self.y > 0:
				self.dir = 90
			elif self.y < 0:
				self.dir = 270
			else:
				self.dir = 0

	def toMat3h(self):
		return np.array([[self.x],[self.y],[self.z],[1]])

	def __repr__(self):
		return f"Vector ({self.x},{self.y})"

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, other):

		if other == 0:
			return Vector(0,0)

		if type(other) in [int,float,np.float64]:
			return Vector(self.x * other, self.y * other, self.z * other)
		elif type(other) == Vector:
			print('yes')
			return self.x * other.x + self.y * other.y + self.z * other.z
		else: print(type(other))

	def __rmul__(self, other):
		return self * other

	def __matmul__(self, other):
		return Vector(self.y * other.z - self.z * other.y,
		              self.z * other.x - self.x * other.z,
		              self.x * other.y - self.y * other.x)


def toVector(mag, dir):
	import numpy as np
	x = mag * np.cos(dir / (180 / np.pi))
	y = mag * np.sin(dir / (180 / np.pi))
	return Vector(x, y)


def v_Add(v1: Vector, v2: Vector):
	return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)


def v_Sub(v1: Vector, v2: Vector):
	return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)


def v_dMul(v1: Vector, v2: Vector):
	return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def v_sMul(v1: Vector, s):
	return Vector(v1.x * s, v1.y * s, v1.z * s)


def v_cMul(v1: Vector, v2: Vector):
	return Vector(v1.y * v2.z - v1.z * v2.y,
	              v1.z * v2.x - v1.x * v2.z,
	              v1.x * v2.y - v1.y * v2.x)


def v_Unit(v: Vector):
	return Vector(v.x / v.mag, v.y / v.mag, v.z / v.mag)


def v_Resolve(v1: Vector, v2: Vector):
	v2_n = v_Unit(v2)

	aax_m = v_dMul(v1, v2_n)
	aax_d = v2_n.dir
	pax_n = toVector(v2_n.mag, v2_n.dir + 90)
	pax_m = v_dMul(v1, pax_n)
	pax_d = pax_n.dir

	v_aax = toVector(aax_m, aax_d)
	v_pax = toVector(pax_m, pax_d)

	return v_aax, v_pax


def Vupdate(l=Vector):
	l.mag = np.sqrt(l.x**2 + l.y**2 + l.z**2)
	if l.x != 0:
		if l.y != 0:
			# if x>0 and y>0:
			l.dir = np.arctan(l.y / l.x) * (180 / np.pi)
			if l.x < 0:
				l.dir = 180 + np.arctan(l.y / l.x) * (180 / np.pi)


if __name__ == '__main__':
	x1 = Vector(4, -2)
	x2 = Vector(4, -4)
	print(x1 * 323.9)

