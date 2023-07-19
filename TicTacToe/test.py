import math

a1 = 62000
n = 12
d = 2000

an = 76

print(int(n * (2 * a1 + (n - 1) * d) / 2))

n = ((an - a1) / d) + 1

print(int(n * (2 * a1 + (n - 1) * d) / 2))

P = 174000
r = 5
n = 1
t = 14
print(round(P * math.pow(1 + (0.01 * r / n), n * t), 0))

# print(P * math.exp(r*t))
# # print(P * math.pow(r, n))
#
# a1 = 5
# r1 = 3
# n1 = 8
# print(a1 * (math.pow(r1, n1) - 1) / (r1 - 1))
