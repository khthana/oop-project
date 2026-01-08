#!/usr/bin/env python3
"""Simple Fibonacci script.

Usage:
  python first.py            # prints first 100 Fibonacci terms
  python first.py --terms 10 # prints first 10 terms
  python first.py --max 100  # prints Fibonacci numbers <= 100
"""
import argparse
import sys


def fib_terms(n):
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def fib_up_to(max_value):
    a, b = 1, 1
    while a <= max_value:
        yield a
        a, b = b, a + b


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print Fibonacci numbers")
    parser.add_argument('--terms', type=int, help='Print first N terms')
    parser.add_argument('--max', type=int, dest='max_value', help='Print Fibonacci numbers up to this max (inclusive)')
    args = parser.parse_args(argv)

    if args.terms is None and args.max_value is None:
        args.terms = 100

    if args.terms is not None:
        if args.terms < 1:
            print('`--terms` must be >= 1', file=sys.stderr)
            return 1
        for v in fib_terms(args.terms):
            print(v)
    else:
        if args.max_value < 1:
            print('`--max` must be >= 1', file=sys.stderr)
            return 1
        for v in fib_up_to(args.max_value):
            print(v)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
