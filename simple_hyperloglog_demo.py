# coding: utf-8
# simple_hyperloglog_demo.py

from simple_hyperloglog import *
from uuid import uuid4
from textwrap import dedent

class DemoHyperLogLog(HyperLogLog):
    def describe_self(self):
        print dedent("""\
        {0}
        HyperLogLogを初期化
        {1}
        誤差: {2}
        p: {3}
        m: {4}
        α: {5}
        で初期化されました\
        """).format("="*80, "-"*80, self.error, self.p, self.m, self.alpha)

    def describe_hll_add(self, key):
        hash_val = mmh3.hash(key)
        bin_index = hash_val & (self.m - 1)
        w = mmh3.hash(key) >> self.p
        rho = get_rho(w)
        print dedent("""\
        {0}
        # key: {2} をHyperLogLogに追加する手順
        {1}
        {2} をハッシュ関数(mmh3.hash())に投入 - 32bitレンジの出力
        得られたハッシュ値は {3}
        {1}
        ハッシュ値にbit-wise AND (m - 1)することでbin-indexを取り出す、つまり
        {3: 032b}
        bit-wise AND
        {4: 032b}
        {1}
        bin-index =
        {5: 032b}
        bin-index取得に使ったpビットを切り捨てる ※ m = 2 ^ p
        w = {6: b}
        {1}
        1が立っている最小位置(インデックスは) {7}
        {1}
        M[bin-index]より大きければ追加する
        M[bin-index] : rho => {8} : {7}\
        """).format("="*80, "-"*40, key, mmh3.hash(key), (self.m - 1),
                    bin_index, w, rho, self.M[bin_index])

    def describe_hll_cardinality(self):
        print dedent("""\
        {0}
        HLLでカーディナリティを推定する手順
        調和平均の値(E) = {2}
        {1}
        補正適用判定
        {3}
        {1}
        カーディナリティ推定値: {4}
        """).format("="*80, "-"*40, self.get_raw_estimate(),
                    self._card_message_switcher(self.get_raw_estimate()),
                    self.__len__())

    def _card_message_switcher(self, E):
        if E <= ((5./2) * self.m): # small range correction
            return "補正あり: 推定値が小さい場合の補正を適用"
        elif E <= ((1./30) * (2 ** 32)):
            return "補正なし: そのままの値"
        else: # large range correction
            return "補正あり: 推定値が大きい場合の補正を適用"

demo_hll = DemoHyperLogLog(0.01)
demo_hll.describe_self()
real_set = set()
for _ in xrange(50000 - 1):
    key = str(uuid4())
    demo_hll.add(key)
    real_set.add(key)
test_key = str(uuid4())
demo_hll.describe_hll_add(test_key)
real_set.add(test_key)
demo_hll.describe_hll_cardinality()
print dedent("""\
HLLでの推定値: {0}
本来の値: {1}
誤差: {2:4f}
""").format(len(demo_hll), len(real_set),
            (len(demo_hll) - len(real_set))/float(len(real_set)))
