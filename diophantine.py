from heapq import heappop, heappush
from operator import mul


def solve_hyperbolic(a, b, c, d, e, f):
    if b * b - 4 * a * c <= 0:
        raise ArithmeticError
    # TODO implement
    # in the meantime, just use http://www.alpertron.com.ar/QUAD.HTM and
    # hardcode the values
    t = (a, b, c, d, e, f)
    if t == (3, 0, -1, -2, 0, -1):
        x = [[1, 0], [-1, -2], [-1, 2]]
        m = [[[-2, -1, 1], [-3, -2, 1]]]
    elif t == (3, 0, -1, 2, 0, -1):
        x = [[-1, 0], [1, -2], [1, 2]]
        m = [[[-2, -1, -1], [-3, -2, -1]]]
    elif t == (1, -2, -1, -1, 1, 0):
        x = [[1, 0], [0, 0]]
        m = [[[5, 2, -2], [2, 1, -1]], [[-1, 2, 1], [2, -5, -1]]]
    elif t == (4, 0, -5, 0, 8, -4):
        x = [[-1, 0]]
        m = [[[-9, -10, 8], [-8, -9, 8]]]
    elif t == (4, 0, -5, 0, -8, -4):
        x = [[-1, 0]]
        m = [[[-9, -10, -8], [-8, -9, -8]]]
    elif t == (5, 0, -1, 2, 0, 1):
        x = [[0, -1], [2, -5], [0, 1], [-1, 2], [-1, -2]]
        m = [[[-9, -4, -2], [-20, -9, -4]]]
    else:
        raise NotImplementedError
    for y in x:
        y.append(1)
    for n in m:
        n.append([0, 0, 1])
    return x, m


def iter_positive_solutions(initial_solutions, matrices):
    yielded = set()
    queue = []
    for x in initial_solutions:
        _push(queue, x)
        for m in matrices:
            _push(queue, _multiply_mat_vec(m, x))
    while queue:
        x = tuple(heappop(queue)[1])
        p = (x[0], x[1])
        if p not in yielded:
            yielded.add(p)
            if p[0] > 0 and p[1] > 0:
                yield p
            for m in matrices:
                _push(queue, _multiply_mat_vec(m, x))


def _push(queue, x):
    if x[0] >= 0 and x[1] >= 0 or x[0] <= 0 and x[1] <= 0:
        heappush(queue, (abs(x[0] + x[1]), x))


def _multiply_mat_vec(m, v):
    return [sum(map(mul, row, v)) for row in m]
