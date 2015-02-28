# coding: utf-8
# simple_bloom_filter.py

from math import ceil, log
from random import randint
import mmh3
import bitarray


class BloomFilter(object):
    def __init__(self, capacity, error=0.005):
        """
        :param capacity: 要素数
        :param error: 偽陽性確率、デフォルト0.5%
        """
        self.capacity = capacity    # デモ用に保存
        self.error = error          # デモ用に保存
        self.num_hashes = int(ceil(log(1.0 / error, 2)))
        self.bits_per_level = int(ceil((capacity * abs(log(error))) /
                                  (self.num_hashes * (log(2) ** 2))))
        self.num_bits = self.num_hashes * self.bits_per_level
        self.bitarray = bitarray.bitarray(self.num_bits)
        self.bitarray.setall(False)

    def _indexes(self, key):
        """
        :param key: ハッシュ化する文字列
        ハッシュ関数はMurmurHash3を利用。MD5やSHAなどでもよい。
        num_hashesの数だけ戻り値として得られる2つの64bitハッシュ値をダブルハッシングし、
        インデックスを返すジェネレータ
        """
        h1, h2 = mmh3.hash64(key)
        for i in xrange(self.num_hashes):
            yield (h1 + i * h2) % self.bits_per_level

    def add(self, key):
        """
        :param key: ブルームフィルタに追加する文字列
        _indexes(key)の戻り値の位置にあるビットを1(=True)にする
        """
        offset = 0
        for index in self._indexes(key):
            self.bitarray[index + offset] = True
            offset += self.bits_per_level

    def __contains__(self, key):
        """
        :param key: ブルームフィルタに含まれているか確認する文字列
        ハッシュ化先の位置全てが1であればTrueを、どれか一つでも0であればFalseを返す
        """
        offset = 0
        for index in self._indexes(key):
            if not self.bitarray[index + offset]:
                return False
            offset += self.bits_per_level
        return True
