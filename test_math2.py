import itertools

import pytest
from eulerlib.math2 import (binomial_coefficient, count_divisors, expmod,
                            factorize, iter_primes, is_prime, more_primes,
                            prime_iterator)

primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
    67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
    229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
    313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401,
    409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
    499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
    601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683,
    691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
    907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
]


def test_prime_iterator():
    iter = prime_iterator(100)
    for p in primes:
        assert p == next(iter)
    iter.reset()
    for p in primes:
        assert p == next(iter)
    assert primes[0] != next(iter)


def test_prime_iterator_small_n():
    iter = prime_iterator(3)
    for p in primes:
        assert p == next(iter)


def test_prime_iterator_large_n():
    iter = prime_iterator(100000)
    for p in primes:
        assert p == next(iter)


def test_iter_primes():
    assert list(iter_primes(2)) == []
    assert list(iter_primes(3)) == [2]
    assert list(iter_primes(5)) == [2, 3]
    assert list(iter_primes(6)) == [2, 3, 5]
    assert list(iter_primes(7)) == [2, 3, 5]
    assert list(iter_primes(8)) == [2, 3, 5, 7]
    assert list(iter_primes(28)) == [2, 3, 5, 7, 11, 13, 17, 19, 23]
    assert list(iter_primes(101)) == [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
        61, 67, 71, 73, 79, 83, 89, 97
    ]


def test_more_primes():
    lt = lambda x: lambda y: y < x
    primes_lt100 = list(itertools.takewhile(lt(100), primes))
    p = list(primes_lt100)
    more_primes(p, 50)
    assert p == primes_lt100
    more_primes(p, 101)
    assert p == primes_lt100
    more_primes(p, 122)
    assert p == list(itertools.takewhile(lt(114), primes))
    p = []
    with pytest.raises(IndexError):
        more_primes(p, 999)


def test_expmod():
    assert expmod(3, 1, 7) == 3
    assert expmod(3, 2, 7) == 2
    assert expmod(3, 3, 7) == 6
    assert expmod(3, 4, 7) == 4
    assert expmod(3, 5, 7) == 5
    assert expmod(3, 6, 7) == 1
    assert expmod(3, 7, 7) == 3
    assert expmod(1, 0, 5) == 1
    assert expmod(2, 2, 2) == 0
    assert expmod(21, 7, 45) == 36
    assert expmod(21, 12, 45) == 36
    assert expmod(100, 100, 10) == 0
    assert expmod(100, 100, 7) == 2


def test_is_prime():
    for p in primes:
        assert is_prime(p)
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(7)
    assert is_prime(89)
    assert is_prime(2551)
    assert is_prime(4217)
    assert is_prime(48157)
    assert is_prime(104729)
    assert is_prime(104729)
    assert is_prime(611953)
    assert not is_prime(4)
    assert not is_prime(100)
    assert not is_prime(447)
    assert not is_prime(1281)
    assert not is_prime(2343)
    assert not is_prime(10455)
    assert not is_prime(310367)


def test_factorize():
    assert list(factorize(1)) == []
    assert list(factorize(2)) == [(2, 1)]
    assert list(factorize(12)) == [(2, 2), (3, 1)]
    assert list(factorize(64)) == [(2, 6)]
    assert list(factorize(640)) == [(2, 7), (5, 1)]
    assert list(factorize(9999)) == [(3, 2), (11, 1), (101, 1)]
    assert list(factorize(15750)) == [(2, 1), (3, 2), (5, 3), (7, 1)]


def test_count_divisors():
    assert count_divisors(1) == 1
    assert count_divisors(2) == 2
    assert count_divisors(4) == 3
    assert count_divisors(5) == 2
    assert count_divisors(24) == 8
    assert count_divisors(53) == 2
    assert count_divisors(120) == 16
    assert count_divisors(1732) == 6
    assert count_divisors(3717) == 12


def test_binomial_coefficient():
    assert binomial_coefficient(10, 3) == 120
    assert binomial_coefficient(43, 21) == 1052049481860
    assert binomial_coefficient(121, 97) == 13562231801970983941985175
