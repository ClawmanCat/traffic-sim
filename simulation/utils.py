import math


class Box:
    def __init__(self, min, max):
        self.min = min
        self.max = max


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


def clamp(x, min_value, max_value):
    if x < min_value: x = min_value
    if x > max_value: x = max_value
    return x


def is_in_box(position, box):
    for pos, min, max in zip(position, box.min, box.max):
        if pos < min or pos > max: return False

    return True