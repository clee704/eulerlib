from fractions import gcd
from functools import reduce
from math import factorial, log, modf, sqrt
from operator import mul
from random import randint


def product(iterable):
    return reduce(mul, iterable, 1)


def digits(n, base=10):
    """Return a list of digits of n in base b notation.

    digits(1437[, 10]) --> [1, 4, 3, 7]
    digits(0xf7, 16) --> [15, 7]

    """
    lst = rdigits(n, base)
    lst.reverse()
    return lst


def rdigits(n, base=10):
    """Return a list of digits of n in base b notation in reversed order.
    If the order of digits does not matter, use this instead of digits()
    for better performance.

    rdigits(1437[, 10]) --> [7, 3, 4, 1]
    rdigits(0367, 8) --> [7, 6, 3]

    """
    lst = []
    if n == 0:
        lst.append(0)
    while n:
        n, d = divmod(n, base)
        lst.append(d)
    return lst


def digits_to_number(iterable, base=10):
    n = 0
    for d in iterable:
        n *= base
        n += d
    return n


def is_square(n):
    return modf(sqrt(n))[0] == 0


def is_pentagonal(n):
    return modf((1 + sqrt(1 + 24 * n)) / 6)[0] == 0


def is_hexagonal(n):
    return modf((1 + sqrt(1 + 8 * n)) / 4)[0] == 0


def continued_fraction(n):
    """Return the continued fraction of the positive square root of n."""
    r = sqrt(n)
    a0 = int(r)
    cycle = []
    if a0 < r:
        a = a0
        b = 1
        # remainder = (sqrt(n) - a) / b
        while b != 1 or not cycle:
            b = (n - a ** 2) // b
            x = int((r + a) // b)
            cycle.append(x)
            a = x * b - a
    return (a0, tuple(cycle))


def generate_convergents(a0, iterator):
    n1, n0 = 1, a0
    d1, d0 = 0, 1
    for x in iterator:
        yield (n0, d0)
        n1, n0 = n0, x * n0 + n1
        d1, d0 = d0, x * d0 + d1


def binomial_coefficient(n, k):
    return factorial(n) // factorial(k) // factorial(n - k)


def multinomial_coefficient(n, ks):
    # Precondition: sum(ks) == n (not checked in this function)
    c = factorial(n)
    for k in ks:
        c //= factorial(k)
    return c


def count_permutations(iterable):
    """Return the number of permutations of the sequence. The sequence
    must be sorted so that equal elements are not seperated by other
    elements in the sequence.

    The result of this function with a sequence can be also obtained by
    counting equal elements in the sequence and using
    multinomial_coefficient().

    count_permutations([0, 1, 2, 3, 4]) --> 120
    count_permutations([1, 2, 2, 3, 3]) --> 30

    """
    n = 1
    m = 1
    last_item = None
    for k, item in enumerate(iterable, 1):
        n *= k
        if item != last_item:
            m = 1
        else:
            m += 1
            n //= m
        last_item = item
    return n


def solve_linear_congruence(a, c, m):
    c = c % m
    d = gcd(a, c)
    e = gcd(d, m)
    if e > 1:
        a //= e
        c //= e
        m //= e
        d //= e
    if d > 1:
        a //= d
        c //= d
    ai = inverse_mod(a, m)
    return ((ai * c) % m, m) if ai is not None else None


def inverse_mod(a, m):
    y2 = 0
    y1 = 1
    n = m
    while a:
        q, r = divmod(n, a)
        y = y2 - q * y1
        y2 = y1
        y1 = y
        n = a
        a = r
    return y2 % m if n == 1 else None


def generate_primes(n):
    """Generate all prime numbers less than n."""
    if n <= 2:
        return iter([])
    sieve = [0, 1] * ((n + 1) >> 1)
    sieve[1] = 0
    sieve[2] = 1
    if n & 1:
        sieve.append(0)
    i = 3
    q = i * i
    while q <= n:
        if sieve[i]:
            for j in range(q, n, i << 1):
                sieve[j] = 0
        i += 2
        q += (i << 2) - 4
    return (m for m in range(n) if sieve[m])


def more_primes(primes, n):
    """Extend the list of prime numbers so that the list contains
    all prime numbers less than n.

    The list must meet the following properties: 1) It must have all
    prime numbers less than some m <= n and m > 2, in ascending order.
    2) n <= p * p where p is the largest prime number in the list.

    """
    a = primes[-1] + 1
    b = n - a
    if b <= 0:
        return
    sieve = ([1, 0] if a & 1 else [0, 1]) * (b >> 1)
    if b & 1:
        sieve.append(a & 1)
    prime_iter = iter(primes)
    next(prime_iter)   # drop 2
    for p in prime_iter:
        q = p * p
        if q > n:
            break
        k = q - a if q >= a else -(a % -p)
        if k & 1 == a & 1:
            k += p
        for j in range(k, b, p << 1):
            sieve[j] = 0
    for b in range(b):
        if sieve[b]:
            primes.append(a + b)


class prime_iterator(object):
    """Prime number iterator supporting efficient re-iterating
    from the first number.

    """

    def __init__(self, n=10000):
        """Initialize an iterator.

        First, it generates a list of all prime numbers less than n
        in ascending order. It includes approximately n / log(n) numbers.
        Whenever the iterator served all numbers in the list, it extends
        the list by adding more (also approximately n / log(n)) prime numbers
        into the list.

        The least possible value for n is 3, although higher value is
        recommended for performance.

        """
        if n < 3:
            raise ValueError('too small n: {0}'.format(n))
        self._p = list(generate_primes(n))
        self._len = len(self._p)
        self._i = 0
        self._n = n
        self._a = n

    def reset(self):
        self._i = 0

    def _augment(self):
        p = self._p
        n = self._n
        a = self._a
        m = int(log(n) / log(a) * a)
        more_primes(p, n + m)
        self._len = len(p)
        self._n += m

    def __iter__(self):
        return self

    def __next__(self):
        p = self._p
        i = self._i
        self._i += 1
        while i == self._len:
          self._augment()
        return p[i]


def is_prime(n, k=10):
    """Return True if n passes the Miller-Rabin primality test,
    which means n is probably prime.

    It never returns False if n is prime. If n is composite, it returns
    False most of the time, but may return True with the probability p <=
    4 ** -k (in the worst case; usually much less than 4 ** -k).

    """
    if n == 2 or n == 3:
        return True
    if not n & 1 or n < 2:
        return False
    m = n - 1
    s = 1
    d = m >> 1
    while not d & 1:
        s += 1
        d >>= 1
    for i in range(k):
        a = randint(2, n - 2)
        x = expmod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(1, s):
            x = x * x % n
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True


def expmod(b, e, m):
    """Compute (b ** e) % m where b, e, and m must be positive integers."""
    r = 1
    while e:
        if e & 1:
            r = r * b % m
        e >>= 1
        b = b * b % m
    return r


def factorize(n):
    """Return a list of tuples (p0, e0), (p1, e1), ..., (pm, em)
    where p0 < p1 < ... < pm are prime numbers and
    n = (p0 ** e0) * (p1 ** e1) * ... * (pm ** em).

    factorize(12) --> [(2, 2), (3, 1)]
    factorize(15750) --> [(2, 1), (3, 2), (5, 3), (7, 1)]

    """
    it = _factorize_prime_iterator
    factors = []
    it.reset()
    for p in it:
        if n == 1 or n < p * p:
            break
        if n % p == 0:
            n //= p
            m = 1
            while n % p == 0 and n > 1:
                n //= p
                m += 1
            factors.append((p, m))
    if n > 1:
        factors.append((n, 1))
    return factors
_factorize_prime_iterator = prime_iterator()


def divisors(n):
    """Return a list of the divisors of n in ascending order."""
    d = [1]
    for p, e in factorize(n):
        l = len(d)
        d.extend(x * p for i in range(e) for x in d[-l:])
    d.sort()
    return d


def count_divisors(n):
    """Return the number of positive divisors of n."""
    # for n = (p ** a) * (q ** b) * ... * (r ** c),
    # number of positive divisors of n = (a + 1) * (b + 1) * ... * (c + 1)
    return reduce(mul, (e + 1 for (p, e) in factorize(n)), 1)


def sum_divisors(n):
    """Return the sum of positive divisors of n."""
    # for n = (p ** a) * ... * (q ** b),
    # sum of positive divisors of n
    #   = (p ** (a + 1) - 1) // (p - 1) * ... * (q ** (b + 1) - 1) // (q - 1)
    g = ((p ** (e + 1) - 1) // (p - 1) for p, e in factorize(n))
    return reduce(mul, g, 1)


def proper_divisor_sums(n):
    """Return a list of sums of proper divisors of positive integers below n.
    """
    lst = [1] * n
    lst[0] = 0
    lst[1] = 0
    for a in range(2, (n + 1) // 2):
        for b in range(2 * a, n, a):
            lst[b] += a
    return lst
