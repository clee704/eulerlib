#! /usr/bin/env python3
import unittest, prime
import itertools


primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
    67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
    229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
    313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401,
    409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
    499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
    601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683,
    691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
    907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]


class test_prime_iterator(unittest.TestCase):

    def test_normal(self):
        iter = prime.prime_iterator(100)
        for p in primes:
            self.assertEqual(p, next(iter))
        iter.reset()
        for p in primes:
            self.assertEqual(p, next(iter))
        self.assertNotEqual(primes[0], next(iter))

    def test_small_n(self):
        iter = prime.prime_iterator(3)
        for p in primes:
            self.assertEqual(p, next(iter))

    def test_large_n(self):
        iter = prime.prime_iterator(100000)
        for p in primes:
            self.assertEqual(p, next(iter))


class test_prime_functions(unittest.TestCase):

    def test_primes(self):
        self.assertListEqual(list(prime.generate_primes(2)), [])
        self.assertListEqual(list(prime.generate_primes(3)), [2])
        self.assertListEqual(list(prime.generate_primes(5)), [2, 3])
        self.assertListEqual(list(prime.generate_primes(6)), [2, 3, 5])
        self.assertListEqual(list(prime.generate_primes(7)), [2, 3, 5])
        self.assertListEqual(list(prime.generate_primes(8)), [2, 3, 5, 7])
        self.assertListEqual(list(prime.generate_primes(28)),
            [2, 3, 5, 7, 11, 13, 17, 19, 23])
        self.assertListEqual(list(prime.generate_primes(101)),
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
            61, 67, 71, 73, 79, 83, 89, 97])

    def test_more_primes(self):
        lt = lambda x: lambda y: y < x
        primes_lt100 = list(itertools.takewhile(lt(100), primes))
        p = list(primes_lt100)
        prime.more_primes(p, 50)
        self.assertListEqual(p, primes_lt100)
        prime.more_primes(p, 101)
        self.assertListEqual(p, primes_lt100)
        prime.more_primes(p, 122)
        self.assertListEqual(p, list(itertools.takewhile(lt(114), primes)))
        p = []
        with self.assertRaises(Exception):
            prime.more_primes(p, 999)

    def test_expmod(self):
        self.assertEqual(prime.expmod(3, 1, 7), 3)
        self.assertEqual(prime.expmod(3, 2, 7), 2)
        self.assertEqual(prime.expmod(3, 3, 7), 6)
        self.assertEqual(prime.expmod(3, 4, 7), 4)
        self.assertEqual(prime.expmod(3, 5, 7), 5)
        self.assertEqual(prime.expmod(3, 6, 7), 1)
        self.assertEqual(prime.expmod(3, 7, 7), 3)
        self.assertEqual(prime.expmod(1, 0, 5), 1)
        self.assertEqual(prime.expmod(2, 2, 2), 0)
        self.assertEqual(prime.expmod(21, 7, 45), 36)
        self.assertEqual(prime.expmod(21, 12, 45), 36)
        self.assertEqual(prime.expmod(100, 100, 10), 0)
        self.assertEqual(prime.expmod(100, 100, 7), 2)

    def test_is_prime(self):
        for p in primes:
            self.assertTrue(prime.is_prime(p))
        self.assertTrue(prime.is_prime(2))
        self.assertTrue(prime.is_prime(3))
        self.assertTrue(prime.is_prime(5))
        self.assertTrue(prime.is_prime(7))
        self.assertTrue(prime.is_prime(89))
        self.assertTrue(prime.is_prime(2551))
        self.assertTrue(prime.is_prime(4217))
        self.assertTrue(prime.is_prime(48157))
        self.assertTrue(prime.is_prime(104729))
        self.assertTrue(prime.is_prime(104729))
        self.assertTrue(prime.is_prime(611953))
        self.assertFalse(prime.is_prime(4))
        self.assertFalse(prime.is_prime(100))
        self.assertFalse(prime.is_prime(447))
        self.assertFalse(prime.is_prime(1281))
        self.assertFalse(prime.is_prime(2343))
        self.assertFalse(prime.is_prime(10455))
        self.assertFalse(prime.is_prime(310367))

    def test_factorize(self):
        self.assertListEqual(list(prime.factorize(1)), [])
        self.assertListEqual(list(prime.factorize(2)), [(2, 1)])
        self.assertListEqual(list(prime.factorize(12)), [(2, 2), (3, 1)])
        self.assertListEqual(list(prime.factorize(64)), [(2, 6)])
        self.assertListEqual(list(prime.factorize(640)), [(2, 7), (5, 1)])
        self.assertListEqual(list(prime.factorize(9999)),
            [(3, 2), (11, 1), (101, 1)])
        self.assertListEqual(list(prime.factorize(15750)),
            [(2, 1), (3, 2), (5, 3), (7, 1)])

    def test_count_divisors(self):
        self.assertEqual(prime.count_divisors(1), 1)
        self.assertEqual(prime.count_divisors(2), 2)
        self.assertEqual(prime.count_divisors(4), 3)
        self.assertEqual(prime.count_divisors(5), 2)
        self.assertEqual(prime.count_divisors(24), 8)
        self.assertEqual(prime.count_divisors(53), 2)
        self.assertEqual(prime.count_divisors(120), 16)
        self.assertEqual(prime.count_divisors(1732), 6)
        self.assertEqual(prime.count_divisors(3717), 12)


if __name__ == '__main__':
    unittest.main()
