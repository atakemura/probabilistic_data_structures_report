# coding: utf-8
# simple_count_min_demo.py

from simple_count_min import *
from uuid import uuid4
from textwrap import dedent
from random import randint
from itertools import chain

class DemoCountMinSketch(CountMinSketch):
    def describe_self(self):
        print dedent("""\
        {0}
        Count-Min Sketchを初期化
        {1}
        δ (delta): {2}
        ε (epsilon): {3}
        幅 (width): {4}
        深さ (depth): {5}
        総カウンタ数: {6}
        で初期化されました\
        """).format("="*80, "-"*80, self.delta, self.epsilon, self.width,
                    self.depth, self.width * self.depth)

    def describe_countmin_update(self, key, count):
        print dedent("""\
        {0}
        # key, count: {1}, {2} をCountMin Sketchに追加する手順
        {1} をハッシュ関数(mmh3.hash64())に投入
        得られた2つのハッシュ値は {3[0]} と {3[1]}\
        """).format("-"*80, key, count, mmh3.hash64(key))
        for row in xrange(self.depth):
            print dedent("""\
            レイヤ {0:2d} でのインデックス => ({1[0]} + {0} * {1[1]}) mod {2} = {3}
            レイヤ {0:2d} の {4:2d} 番目のカウンタに {5:2d} を追加\
            """).format(row, mmh3.hash64(key), self.width,
                        self._index(row, key), self._index(row, key) + 1, count)
        sketch_before_update = self.wrap_list(self.sketch)
        self.update(key, count)
        sketch_after_update = self.wrap_list(self.sketch)
        print "{0}: {1}".format("アップデート前, before", "".join(map(str, sketch_before_update)))
        print "{0}: {1}".format("アップデート後, after", "".join(map(str, sketch_after_update)))


    def describe_countmin_get(self, key):
        print dedent("""\
        {0}
        # key: {1} の出現回数をクエリする手順
        {1} をハッシュ関数(mmh3.hash64())に投入
        得られた2つのハッシュ値は {2[0]} と {2[1]}\
        """).format("-"*80, key, mmh3.hash64(key))
        counter_list = []
        for row in xrange(self.depth):
            print dedent("""\
            レイヤ {0:2d} でのインデックス => ({1[0]} + {0} * {1[1]}) mod {2} = {3}
            レイヤ {0:2d} の {4:2d} 番目のカウンタの値を取得\
            """).format(row, mmh3.hash64(key), self.width,
                        self._index(row, key), self._index(row, key) + 1)
            counter_list.append(self.sketch[row][self._index(row, key)])
        print "カウンタの値のリスト: {0}".format("".join(map("{:3d}".format, counter_list)))
        print "リストから最小値を選択し結果とする: {0}".format(min(counter_list))

    def wrap_list(self, sketch):
        output_list = list(chain.from_iterable([map("{:3d}".format, row) for row in sketch]))
        for row in xrange(self.depth):
            output_list.insert(self.width * row + row, "\n")
        return output_list


demo_countmin = DemoCountMinSketch(0.1, 0.1)
demo_countmin.describe_self()
demo_stream = []
for _ in xrange(50): # デモ用にストリームを予めいくつか処理し、カウンタを埋める
    demo_stream.append((str(uuid4()), randint(1, 10)))
for datum in demo_stream:
    demo_countmin.update(*datum)
test_datum = (demo_stream[-1][0], randint(1, 20))
real_count = demo_stream[-1][1] + test_datum[1]
demo_countmin.describe_countmin_update(*test_datum)
demo_countmin.describe_countmin_get(test_datum[0])
print dedent("""\
キー: {0}
本来の値: {1}
CMSketchの値: {2}
""").format(test_datum[0], real_count, demo_countmin.get(test_datum[0]))
