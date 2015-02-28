# coding: utf-8
# simple_bloom_filter_demo.py

from simple_bloom_filter import *
from uuid import uuid4
from textwrap import dedent
from itertools import chain

class DemoBloomFilter(BloomFilter):
    def describe_self(self):
        print dedent("""\
        {0}
        Bloom filter初期化
        {1}
        要素数: {2}
        偽陽性確率: {3:.2%}
        レイヤの数: {4}
        レイヤごとのビット数: {5}
        総ビット数: {6}
        で初期化されました\
        """).format("="*80, "-"*80, self.capacity, self.error,
                    self.num_hashes, self.bits_per_level, self.num_bits)

    def describe_bloom_add(self, key):
        print dedent("""\
        {0}
        # {1} をBloom filterに追加する手順
        {1} をハッシュ関数(mmh3.hash64())に投入
        得られた2つのハッシュ値は {2[0]} と {2[1]}\
        """).format("-"*80, key, mmh3.hash64(key))

        to_update = bitarray.bitarray(self.num_bits)
        to_update.setall(False)
        add_offset = 0
        for index in self._indexes(key):
            to_update[index + add_offset] = True
            add_offset += self.bits_per_level

        for layer, index in enumerate(self._indexes(key)):
            print dedent("""\
            レイヤ {0:2d} でのインデックス => ({1[0]} + {0} * {1[1]}) mod {2} = {3}
            レイヤ {0:2d} の {4:2d} ビット目を 1 にセット\
            """).format(layer, mmh3.hash64(key), self.bits_per_level, index, index + 1)

        current_filter = self.wrap_string(self.bitarray.to01())
        update_filter = self.wrap_string(to_update.to01())
        self.add(key)
        post_update_filter = self.wrap_string(self.bitarray.to01())
        print "{0}: {1}".format("現在のフィルタの状態", "".join(map(str, current_filter)))
        print "{0}: {1}".format("アップデート用", "".join(map(str, update_filter)))
        print "{0}: {1}".format("アップデート後のフィルタの状態", "".join(map(str, post_update_filter)))

    def describe_bloom_query(self, key):
        print dedent("""\
        {0}
        # {1} がBloom filterに存在するか確認する手順
        {1} をハッシュ関数(mmh3.hash64())に投入
        得られた2つのハッシュ値は {2[0]} と {2[1]}\
        """).format("-"*80, key, mmh3.hash64(key))

        current_filter = self.wrap_string(self.bitarray.to01())
        print "{0}: {1}".format("現在のフィルタの状態", "".join(map(str, current_filter)))
        query_offset = 0
        for layer, index in enumerate(self._indexes(key)):
            print "レイヤ {0:2d} でのインデックス {1:2d} ビット目が 1 かチェック => {2:2d}".\
                format(layer, index + 1, self.bitarray[index + query_offset])
            query_offset += self.bits_per_level
        print "{0} がBloom filterに存在するか確認した結果 => {1}".format(key, key in self)

    def wrap_string(self, input_string):
        output_list = map("{:2s}".format, list(input_string))
        for layer in xrange(self.num_hashes):
            output_list.insert(self.bits_per_level * layer + layer, "\n")
        return output_list

demo_bloom = DemoBloomFilter(10, 0.05)
demo_bloom.describe_self()
print "="*80 + "\n" + "キーが存在する場合"
for _ in xrange(5): # 半分埋めてハッシュ値の衝突を起きやすくする
    demo_bloom.add(str(uuid4()))
key_to_add = str(uuid4())
demo_bloom.describe_bloom_add(key_to_add)
demo_bloom.describe_bloom_query(key_to_add)
print "="*80 + "\n" + "キーが存在しない場合"
key_to_query = str(uuid4())
demo_bloom.describe_bloom_query(key_to_query)
