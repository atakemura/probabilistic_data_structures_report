# coding: utf-8
# simple_hyperloglog.py

import ctypes
import mmh3
from math import ceil, log

# ctypes.util.find_library("c") => Cライブラリのパス。環境によって違うので注意。
libc = ctypes.cdll.LoadLibrary('/usr/lib/libc.dylib')

def get_rho(w):
    """
    :param w: 対象の値
    最小位から数えて最初の1ビットの位置(1-indexed)
    """
    return libc.ffs(w)

def get_alpha(p):
    """
    :param p: precision、精度に関連したビット数
    定数、alpha_mを返す。m = 2 ** p"""
    if not (4 <= p <= 16):
        raise ValueError("Expected p ∈ [4..16] but got %d" % p)
    alpha_ms = [0.673, 0.697, 0.709]
    if p in (4, 5, 6):
        return alpha_ms[p - 4]
    else:
        return (0.7213 / (1. + 1.079 / (2 ** p)))

def linear_counting(m, v):
    """
    :param m: バケット(estimator)の数、2 ** p
    :param v: 値が0のバケットの数
    small range correction
    """
    return m * log(float(m) / v)

class HyperLogLog(object):
    """
    2007年のHLL論文の擬似コード参照
    Flajolet et al. DMTCS Proc. 2007. 127-146.
    """

    def __init__(self, relative_error):
        """
        :param relative_error: HLLに要求する誤差、[0..1]
        initialize M(0)...M(m - 1) with 0
        relative_error = 1.04 / sqrt(m)
        m = 2 ** p
        i.e. p = log((1.04 / error) ** 2)
        """
        self.error = relative_error # デモ用に保存
        self.p = int(ceil(log((1.04 / relative_error) ** 2, 2)))
        self.m = 2 ** self.p
        self.alpha = get_alpha(self.p)
        self.M = [0 for _ in xrange(self.m)]

    def __len__(self):
        return round(self.estimate_cardinality())

    def add(self, value):
        """
        :param value: HLLに追加する値
        h: D -> {0, 1} ** 32    ; 32-bit hash func with domain D
        x = h(v)                ; hash value
        j = <x_31, ..., x32-p>_2; bin index; ANDで取り出す
        w = <x_31-p, ..., x_0>_2; the rest of the bits; p-bit 右シフト
        M[j] = max(M[j], rho(w));
        """
        hash_value = mmh3.hash(value)
        bin_idx = hash_value & (self.m - 1)
        w = hash_value >> self.p
        self.M[bin_idx] = max(self.M[bin_idx], get_rho(w))

    def get_raw_estimate(self):
        return (self.alpha * self.m ** 2) / sum((2 ** -x) for x in self.M)

    def estimate_cardinality(self):
        E = self.get_raw_estimate()
        if E <= ((5./2) * self.m): # small range correction
            v = self.M.count(0)
            if v != 0:
                return linear_counting(self.m, v)
            else:
                return E
        elif E <= ((1./30) * (2 ** 32)):
            return E
        else: # large range correction
            return -(2 ** 32) * log(1 - (float(E) / (2 ** 32)))