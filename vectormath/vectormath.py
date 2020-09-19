"""
	This file contains the actual math that is used to solve the tasks
	It contains vectors and stuff like this as classes
"""

from math import sqrt

##	calculates the skalar of 2 vectors
##	wrote it like this for better readability
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
	return Vector(x, y, z)


##	calculates the amount of a vector
##	used when checking distance between points with the hessesche normalform
def amount(vector) -> float:
	return sqrt(sum([x ** 2 for x in vector]))


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
		return self.__str__()


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

	def __truediv__(self, factor):
		return Vector(vectorlist = [co / factor for co in self.__iter__()])

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

	def __iter__(self):
		return iter([self.a, self.m])

	def __str__(self):
		return f"G: x = {str(self.a)} + {str(self.rfactor)} * {str(self.m)}"

	def __repr__(self):
		return self.__str__()
		

class PlaneEquation():
	
	def __init__(self, a : Vector, m : Vector = False, v : Vector = False, normvector = False):
		if not m and not v:
			pass
		self.m = m #first factor
		self.v = v #second factor
		self.a = a
		self.rfactor = "r"	##	dont need this
		self.sfactor = "s"	##	dont need this
		self.normvector = crossproduct(m, v) if not normvector else normvector



	def calcfactors(self, point):
		##	this calculates the initial values of the factors 
		##	checking if these values fit in the other equations will happen on a later point

		##	needs to be finished!
		sfactor = (0, 0, 0)
		mfactor = (0, 0, 0)

		for index, (p_value, a_value, m_value, v_value)  in enumerate(zip(point, self.a, self.m, self.v)):
			if m_value == 0 and v_value == 0:
				##	looks if m and v are 0 and if so returns false if p != a
				if p_value != a_value:
					return False
				continue

			elif m_value == 0 or v_value ==0:
				p_value = (p_value - a_value) / self.m if m_value != 0 else (p_value - a_value) / self.v
				factor = ((v_value / m_value) * (-1), p_value, "m") if m_value != 0 else (p_value, 0, "v")

			else:
				pass
				

			#if factor[2] != 


			if m_value < 0:
				factor[0] = factor[0] * (-1)

	##	position of point to vector

	##	used by check_point to determin if the point is on the plane
	##	calculates via the coordinate form
	def check_on_plane(self, point):

		point_side_result = 0
		supposed_result = 0

		for n_cooradinate, point_cooradinate, a_coordinate in zip(self.normvectorm, point, self.a):
			point_side_result += n_coordinate * point_cooradinate
			supposed_result += n_coordinate * a_coordinate * -1
		return point_side_result == supposed_result * -1


	##	calculates the distance between a point and a plane. Returns the distance
	##	uses the hessesche normalform to do this. If you don't know what this is, google it!
	##	this function works!
	def plane_point_distance(self, point):
		result = 0
		n = self.normvector / amount(self.normvector)		##	sets length of n vector to 1
		for self_co, point_co, n_co in zip(self.a, point, n):
			result += n_co * (self_co * -1) + n_co * point_co
		return abs(result)
		

	def check_point(self, point): 
		distance = self.plane_point_distance(point)
			return distance if distance != 0 else True

	##	positon of point to vector end

	##	position of line to plane
	

	def __iter__(self):
		return iter([self.a, self.m, self.v])

	def __str__(self):
		return f"G: x = {str(self.a)} + {str(self.rfactor)} * {str(self.m)} + {str(self.sfactor)} * {str(self.v)}"

	def __repr__(self):
		return self.__str__()

## just for development. Needs to be removed afterwards
if __name__ == "__main__":
	a = Vector(1, 2, 3)
	m = Vector(4, 5, 6)
	v = Vector(7, 8, 9)
	pe = PlaneEquation(a, m, v)