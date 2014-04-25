from itertools import permutations
from .math2 import digits_to_number


def generate_fibonacci(a=1, b=1):
    """Generate a general Fibonacci sequence starting from a and b.

    generate_fibonacci([1[, 1]]) --> 1 1 2 3 5 8 13 ...
    generate_fibonacci(4, 7) --> 4 7 11 18 29 47 ...
    """
    a = a + a - b
    b = b - a
    while 1:
        c = a + b
        yield c
        a = b
        b = c


def generate_polygonal_numbers(r):
    """Generate r-gonal numbers.

    generate_polygonal_numbers(3) --> 1 3 6 10 15 21 ...
    generate_polygonal_numbers(4) --> 1 4 9 16 25 36 ...
    generate_polygonal_numbers(5) --> 1 5 12 22 35 51 ...
    """
    a = 1
    b = 1
    c = r - 2
    while 1:
        yield a
        b += c
        a += b


def generate_nondecreasing_digits():
    """Generate a sequence of positive integers that have digits in
    non-decreasing order, in ascending order. See A009994 in OEIS
    (http://www.research.att.com/~njas/sequences/A009994).
    """
    next = 1
    while 1:
        yield next
        next += 1
        if next % 10 == 0:
            m = next // 10
            k = 1
            while m % 10 == 0:
                m //= 10
                k = k * 10 + 1
            next += m % 10 * k


def generate_nonincreasing_digits():
    """Generate a sequence of positive integers that have digits in
    non-increasing order, in ascending order. See A009996 in OEIS
    (http://www.research.att.com/~njas/sequences/A009996).
    """
    next = 1
    while 1:
        yield next
        m, r = divmod(next, 10)
        if m % 10 == r:
            m //= 10
            k = 10
            while m % 10 == r:
                m //= 10
                k *= 10
            next = (m * 10 + r + 1) * k
        else:
            next += 1


def generate_pandigitals(n):
    """Generate n-digit pandigital numbers in descending order.
    n must be >= 1 and <= 9, or nothing will be generated.

    generate_pandigitals(3) --> 321 312 231 213 132 123
    generate_pandigitals(5) --> 54321 54312 54231 54213 54132 54123 ...
    """
    if not 1 <= n <= 9:
        return
    for p in permutations(range(n, 0, -1)):
        yield digits_to_number(p)


def is_palindromic(x):
    "Return True if x is a palindromic sequence."
    i = 1
    j = len(x) // 2
    while i <= j and x[i - 1] == x[-i]:
        i += 1
    return i > j


def is_pandigital(x, n):
    """Return True if x is a pandigital sequence of length n,
    containing all digits 1 to n.
    """
    seen = [0] * n
    for d in x:
        if not 1 <= d <= n:
            return False
        elif seen[d - 1]:
            return False
        else:
            seen[d - 1] = 1
    return all(seen)
