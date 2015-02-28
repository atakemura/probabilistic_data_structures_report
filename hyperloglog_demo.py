# coding: utf-8
# hyperloglog_demo.py

from simple_hyperloglog import *

hll = HyperLogLog(0.01) # 1%の誤差を許容
print "\t".join(["actual", "HLL estimate", "error"])
for i in xrange(1, 5000001): # 500万
    hll.add(str(i))
    if i % (10**5) == 0 :
        print "\t".join(map(str, [i, len(hll),
                                  (len(hll) - i)/float(i)]))
