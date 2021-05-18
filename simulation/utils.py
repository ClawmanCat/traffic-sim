import math
from functools import partial


class Box:
    def __init__(self, min, max):
        self.min = min
        self.max = max


def minmaxbox(box):
    return Box(
        (min(box.min[0], box.max[0]), min(box.min[1], box.max[1])),
        (max(box.min[0], box.max[0]), max(box.min[1], box.max[1]))
    )


def vec(x, dims = 2):
    return tuple([x] * dims)


def add(a, b):
    result = []

    for x, y in zip(a, b):
        result.append(x + y)

    return result


def sub(a, b):
    result = []

    for x, y in zip(a, b):
        result.append(x - y)

    return result


def mul(a, b):
    result = []

    for x, y in zip(a, b):
        result.append(x * y)

    return result


def div(a, b):
    result = []

    for x, y in zip(a, b):
        result.append(x / y)

    return result


def dot(a, b):
    result = 0

    for x, y in zip(a, b):
        result += x * y

    return result


def mag(v):
    accum = 0
    for e in v: accum += e * e
    return math.sqrt(accum)


def norm(v):
    return div(v, [mag(v)] * len(v))


def project(a, b):
    return mul(b, vec(dot(a, div(b, vec(mag(b))))))


def vec_min(vec, val):
    return tuple(map(partial(min, val), vec))


def vec_max(vec, val):
    return tuple(map(partial(max, val), vec))


def clamp(x, min_value, max_value):
    if x < min_value: x = min_value
    if x > max_value: x = max_value
    return x


def is_in_box(position, box):
    for pos, min, max in zip(position, box.min, box.max):
        if pos < min or pos > max: return False

    return True


# Given two objects, at p1 and p2 respectively, travelling at v1 and v2 respectively,
# calculate if object 1 should start decelerating to avoid a collision, assuming it decelerates at decel.
def should_brake(p1, v1, p2, v2, safety_distance = 20.0, dt = 2.5):
    if v2 >= v1: return False
    return p1 + safety_distance + (v1 * dt) >= p2 + (v2 * dt)