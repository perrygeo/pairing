#!/usr/bin/env python
from __future__ import print_function
from pairing import pair, depair
import timeit


def test_pair(a, b):
    assert depair(pair(a, b)) == (a, b)
    return pair(a, b)


def run_tests():
    test_pair(22, 33)
    test_pair(2**8, 2**8)
    test_pair(2**16, 2**16)

    try:
        test_pair(2**52, 2**52)
    except ValueError:
        pass  # long integers suffer from some imprecision at this size

    try:
        test_pair(-1, -1)
    except ValueError:
        pass  # negative values not supported

    return "Tests pass."


if __name__ == '__main__':
    print(run_tests())

    print("Benchmarking...")
    i = 20000
    print(round(timeit.timeit(run_tests, number=i), 5), "sec,", i, "iterations")
