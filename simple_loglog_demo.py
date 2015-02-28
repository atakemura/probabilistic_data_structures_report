# coding: utf-8
# simple_loglog_demo.py

"""
i: 試行回数
rand_int: 整数、今回は8ビットの表現範囲内
bin(rand_int): rand_intの2進数表記
lsb_one_index: 最小位の1ビットの位置
bitmap: lsb_one_indexを記録したあとのビットマップ
ffs(): ビット文字列内の最初の1の位置(インデックス)を返す。標準Cライブラリ。$ man ffs
"""

import random
import ctypes
# ctypes.util.find_library("c") => Cライブラリのパス。環境によって違う。
libc = ctypes.cdll.LoadLibrary('/usr/lib/libc.dylib')

print "\t".join(["i","rand_int","bin(rand_int)","lsb_one_index","bitmap"])
bitmap = 0
for i in xrange(1, 20):
    random_int = random.randint(0, (2 ** 8) - 1)
    lsb_one_index = libc.ffs(random_int)
    bitmap |= int(2 ** (lsb_one_index - 1))
    print "\t".join(map(str, [i,
                              random_int,
                              "{:08b}".format(random_int),
                              lsb_one_index,
                              "{:08b}".format(bitmap)]))