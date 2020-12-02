#!/usr/bin/env python


"""
A python implementation of the tausworthe generator (TG)

Tausworthe Generator (TG) is a kind of multiplicative recursive generator
which produces random bits

An introduction to TG:
https://homes.luddy.indiana.edu/kapadia/project2/node9.html

TG belongs to LFSRs (linear feedback shift registers).
"""


import numpy as np
from typing import Tuple


__author__ = "Jingquan Wang"
__email__ = "jq.wang1214@gmail.com"


class TG(object):
    def __init__(self, length: int=1, debug: bool=False) -> None:
        """
        Parameters
        ----------
        length : int
                length of generated PRN array
        """
        self.r = self.q = self.l = 0
        self.debug = debug
        if length <= 0:
            raise ValueError("Length must be a positive integer!")
        self.length = length

    def get_bits(self) -> np.ndarray:
        """
        Get raw bits

        """
        return self.B

    def seed(self, r: int = 3, q: int = 5, l: int = 4):
        """
        Define a seed for the PRN generator
        Seeds are defined by r, q and l

        Parameters
        ----------
        r : int
                as defined in
                B[i] = (B[i−r] +B[i−q]) mod 2 = B[i−r] XOR B[i−q] (0 < r < q)
        q : int
                as defined in
                B[i] = (B[i−r] +B[i−q]) mod 2 = B[i−r] XOR B[i−q] (0 < r < q)
        l : int
                lengths of bits in base 2
                Use (l-bits in base 2)/2^l and convert to base 10
        """
        self.r = r
        self.q = q
        self.l = l

    def convert(self, bits: np.ndarray) -> np.ndarray:
        """
        Convert bits into decimals

        Parameters
        ----------
        bits : numpy.ndarray
                bits to be converted
        """
        res = 0
        for index, bit in enumerate(bits):
            res += bit * np.power(2, (len(bits) - index - 1))
        return res

    def random(self) -> np.ndarray:
        """
        Generate random numbers using Tauworthe method
        """

        # check whether seed was initialized
        if self.r == 0 or self.q == 0 or self.l == 0:
            self.seed()

        # length is the number of bits we need
        self.length_bit = self.length * self.l
        self.verbose(f"self.length_bit = {self.length_bit}")

        # initialize the array B
        self.B = np.ones(self.length_bit)

        # extend array B
        for i in range(self.q, self.length_bit):
            new_bit = 1 if self.B[i - self.r] != self.B[i - self.q] else 0
            self.B[i] = new_bit

        self.verbose(f"Before splitting, self.B is {self.B}")

        self.B = np.array_split(self.B, self.length)

        self.verbose(f"After splitting, self.B is {self.B}")

        self.decimal = np.array([self.convert(seg)/np.power(2, self.l) for seg in self.B])

        return self.decimal

    def verbose(self, *args, **kwargs) -> None:
        """
        Customized print function for debug
        """
        if self.debug:
            print(*args, **kwargs)


def main() -> None:
    tg = TG(length=10, debug=True)
    res = tg.random()
    print(res)

if __name__ == "__main__":
    main()





