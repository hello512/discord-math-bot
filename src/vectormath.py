"""
	This file contains the actual math that is used to solve the tasks
	It contains vectors and stuff like this as classes
"""

class Point():
	def __init__(self, x : int = 0, y : int = 0, z : int = 0, pointlist : list = 0):
		if pointlist != 0 and len(pointlist) >= 2:				##	check if vector coordinates are givven in pointlist or as points
			self.x = pointlist[0]
			self.y = pointlist[1]
			self.z = 0 if len(pointlist) == 2 else pointlist[2]	##	puts in 0 if the given vektor is 2 dimensional
		else:
			self.x = x
			self.y = y
			self.z = z

	def __iter__(self):
		return iter([self.x, self.y, self.z])

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z})"	##	return  vector as str like (x, y, z)

	def __repr__(self):
		return self.__str__(Point)

class Vector():
	def __init__(self, x : int = 0, y : int = 0, z : int = 0, vectorlist : list = 0):
		if vectorlist != 0 and len(vectorlist) >= 2:				##	check if vector coordinates are givven in vectorlist or as points
			self.x = vectorlist[0]
			self.y = vectorlist[1]
			self.z = 0 if len(vectorlist) == 2 else vectorlist[2]	##	puts in 0 if the given vektor is 2 dimensional
		else:
			self.x = x
			self.y = y
			self.z = z

	def __add__(self, factor):
		return Vector(self.x + factor.x, self.y + factor.y, self.z + factor.z)

	def __sub__(self, vector2):
		##	return (v1x - v2x, v1y - v2y, v1z - v2z) v1 is this vector ;D
		return Vector(x = self.x - vector2.x, y = self.y - vector2.y, z = self.z - vector2.z)

	##	mutliplyes vector with given factor (must be int)
	def __mul__(self, factor : int):
		return Vector(self.x * factor, self.y * factor, self.z * factor)

	def __iter__(self):
		return iter([self.x, self.y, self.z])

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z})"	##	return  vector as str like (x, y, z)

	def __repr__(self):
		return self.__str__()

class LinearEquation():
	def __init__(self, a, m):
		self.a = a
		self.m = m
		self.rfactor = "r"

	##	this function only works, if all givven points are an int. The only var is r
	##	this function is used by chekcpoint
	##	works !
	def calcfactor(self, point):
		r = []
		for i, (a_value, m_value, p_value) in enumerate(zip(self.a, self.m, point)):
			r.append((p_value - a_value) / m_value)
			if i != 0 and r[i-1] != r[i]:
				return False
		return True

	##	returns True if Point is on the Line, False if not
	##	uses the calcfactor method, to do this
	def checkpoint(self, point):
		return self.calcfactor(point)

	def __str__(self):
		return f"G: x = {str(self.a)} + {str(self.rfactor)} * {str(self.m)}"

class PlaneEquation():
	def __init__(self, a : Vector, m : Vector, v : Vector):
		self.v = v
		self.m = m
		self.a = a
		self.rfactor = "r"
		self.sfactor = "s"

	def checkpoint(self):
		pass




	def __str__(self):
		return f"G: x = {str(self.a)} + {str(self.rfactor)} * {str(self.m)} + {str(self.sfactor)} * {str(self.v)}"


##	calculates the skalar of 2 vectors
##	wrote it like this for better readability
##	if the skalar is 0 the vectors are orthogonal
##	works !
def skalar(vector0, vector1):
	x = vector0.x * vector1.x
	y = vector0.y * vector1.y
	z = vector0.z * vector1.y
	return x + y + z


##	calculates the cross product of two vectors
def crossproduct(vector0, vector1):
	x = vector0.z * vector1.y - vector0.y * vector1.z
	y = vector0.x * vector1.z - vector0.z * vector1.x
	z = vector0.y * vector1.x - vector0.x * vector1.y
	return vector(x, y, z)


