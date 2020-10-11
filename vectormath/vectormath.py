"""
	This file contains the actual math that is used to solve the tasks
	It contains vectors and stuff like this as classes
"""

import math


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
	return math.sqrt(sum([x ** 2 for x in vector]))

##	reutrns angle between two vectors
##	still needs to be checked!
def vector_angle(vec0, vec1):
	try:
		res = skalar(vec0, vec1) / (amount(vec0) * amount(vec1))
	except ZeroDivisionError:
		return 0
	return math.degrees(math.acos(res))

##	returns the angle between plane and line hitting the plane, when giving the n vector of the plane and the m vector of the line
##	still needs to be checked!
def plane_vector_angle(vec0, vec1):
	res = skalar(vec0, vec1) / (amount(vec0) * amount(vec1))
	return math.degrees(math.asin(res))


class Point():
	def __init__(self, x : int = 0, y : int = 0, z : int = 0, pointlist : list = 0):
		if pointlist != 0 and len(pointlist) >= 2:				##	check if vector coordinates are given in pointlist or as points
			self.x = pointlist[0]
			self.y = pointlist[1]
			self.z = 0 if len(pointlist) == 2 else pointlist[2]	##	puts in 0 if the given vektor is 2 dimensional
		else:
			self.x = x
			self.y = y
			self.z = z

	##	build in operations

	def __iter__(self):
		return iter([self.x, self.y, self.z])

	def __str__(self):
		return f"({self.x}, {self.y}, {self.z})"	##	return  vector as str like (x, y, z)

	def __repr__(self):
		return self.__str__()


class Vector():
	def __init__(self, x : int = 0, y : int = 0, z : int = 0, vectorlist : list = 0):
		if vectorlist != 0 and len(vectorlist) >= 2:				##	check if vector coordinates are given in vectorlist or as points
			self.x = vectorlist[0]
			self.y = vectorlist[1]
			self.z = 0 if len(vectorlist) == 2 else vectorlist[2]	##	puts in 0 if the given vektor is 2 dimensional
		else:
			self.x = x
			self.y = y
			self.z = z

	#def normalize(self):
	#	return self.__truediv__(amount(self))
	##	build in operations

	def __add__(self, factor):
		return Vector(self.x + factor.x, self.y + factor.y, self.z + factor.z)

	def __sub__(self, vector2):
		##	return (v1x - v2x, v1y - v2y, v1z - v2z) v1 is this vector ;D
		return Vector(x = self.x - vector2.x, y = self.y - vector2.y, z = self.z - vector2.z)

	##	mutliplyes vector with given factor (must be int)
	def __mul__(self, factor : int):
		return Vector(self.x * factor, self.y * factor, self.z * factor)

	def __truediv__(self, factor):
		##	needs error handling!
		##	returns 0 if division by zero
		try:
			result = Vector(vectorlist = [co / factor if co != 0 else 0 for co in self.__iter__()])
		except ZeroDivisionError:
			raise ZeroDivisionError("your trying to divide by 0!")
		return result

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

	##	this function only works, if all given points are an int. The only var is r
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

	def calc_point(self, factor):
		## calculates point with given factor
		return self.a + self.m * factor

	##	build in operations

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

		self.coo_form_values = self.get_coo_values()


	def get_coo_values(self) -> list:
		##	calculates all the values needed for the param form
		##	works
		value_list = [val for val in self.normvector]
		value_list.append(sum([a_co * n_co for a_co, n_co in zip(self.a, self.normvector)]))
		return value_list

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

		for n_coordinate, point_cooradinate, a_coordinate in zip(self.normvector, point, self.a):
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
	def line_parallel(self, line):
		return skalar(line.m, self.normvector) == 0

	def intercept_point_factor(self, line):
		##	calculates the factor when the line hits the plane
		##	used to get the interception point between the plane and the line
		##	needs to be checked and tested
		dividing_factor, number = 0, 0
		for a_co, m_co, co_form_val in zip(line.a, line.m, self.coo_form_values):
			dividing_factor += co_form_val * m_co
			number += co_form_val * a_co
		return (self.coo_form_values[3] - number) / dividing_factor

	##	not doing anything right now, might be used in later time. Needs to be finished
	def get_intercept_point(self, line):
		factor = self.intercept_point_factor(line)
		pass

	def check_line(self, line):
		if self.line_parallel(line):
			distance = self.plane_point_distance(line.a)
			return ("equal", 0) if distance == 0 else ("parallel", distance)
		else:
			return ("point", line.calc_point(self.intercept_point_factor(line)))

	##	build in operations

	def __iter__(self):
		return iter([self.a, self.m, self.v])

	def __str__(self):
		return f"G: x = {str(self.a)} + {str(self.rfactor)} * {str(self.m)} + {str(self.sfactor)} * {str(self.v)}"

	def __repr__(self):
		return self.__str__()
