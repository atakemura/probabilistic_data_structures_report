# coding: utf-8
# simple_count_min.py

from math import ceil, log, exp
from sys import maxint
import mmh3


class CountMinSketch(object):
    def __init__(self, delta, epsilon):
        """
        :param delta: 上限値を超える誤差が起こる確率; ~0.0001など
        :param epsilon: 誤差上限値の係数; ~0.001など
        """
        self.delta = delta      # デモ用に保存
        self.epsilon = epsilon  # デモ用に保存
        self.depth = int(ceil(log(1 / delta)))
        self.width = int(ceil(exp(1) / epsilon))
        self.sketch = self._initialize_sketch()

    def _initialize_sketch(self):
        """
        全てのカウンタを0で初期化
        """
        sketch = [[0 for _ in xrange(self.width)] for _ in xrange(self.depth)]
        return sketch

    def _index(self, row, key):
        """
        :param row: 行番号
        :param key: ハッシュ値を得るキー
        """
        h1, h2 = mmh3.hash64(key)
        index = (h1 + row * h2) % self.width
        return index

    def update(self, key, count):
        """
        :param key: 更新する値のキー
        :param count: 更新する値に足す値
        """
        for row in xrange(self.depth):
            index = self._index(row, key)
            self.sketch[row][index] += count

    def get(self, key):
        """
        :param key: 推計値を取り出すキー
        """
        value = maxint
        for row in xrange(self.depth):
            index = self._index(row, key)
            value = min(self.sketch[row][index], value)
        return value
