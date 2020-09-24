import sys

sys.path.append("../")
from discord_math_bot.vectormath import vectormath


print("calculating")
v = vectormath.Vector(1, 0, 0)
v2 = vectormath.Vector(-1, 0, 0)
a = vectormath.Vector(0, 0, 1)

p = vectormath.Point(1, 1, 3)

plane = vectormath.PlaneEquation(a, v, v2)
print(plane.plane_point_distance(p))

print("vector angle:", vectormath.vector_angle(v, v2))
