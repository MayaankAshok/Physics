import numpy as np
from Vector import Vector


class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class LineSeg:
    def __init__(self, pos0=(0, 0), pos1=(0, 0)):
        self.pos0 = Vector(pos0[0], pos0[1])
        self.pos1 = Vector(pos1[0], pos1[1])
        self.a = self.pos1.y - self.pos0.y
        self.b = self.pos0.x - self.pos1.x
        self.c = self.pos0.x * (self.pos0.y - self.pos1.y) + self.pos0.y * (self.pos1.x - self.pos0.x)

class AABB:
    def __init__(self,minX,maxX,minY,maxY):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

def toAABB(vMin:Vector,vMax:Vector):
    return AABB(vMin.x,vMin.y,vMax.x,vMax.y)