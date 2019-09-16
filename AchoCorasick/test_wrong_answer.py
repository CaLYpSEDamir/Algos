import os
import re
import sys
import time
import math
import random
from collections import defaultdict

from trie import ACTrie


# file = 'test_case_1823728075410_1823728075410.txt'
file = 'test_case_runtime_error_0_8652768.txt'

if __name__ == '__main__':

    dnas = []
    min_ = None
    max_ = None

    with open(file) as f:
        n = f.readline()
        genes = f.readline().rstrip().split()
        health = list(map(int, f.readline().rstrip().split()))

        words_cnt = int(f.readline())

        for _ in range(words_cnt):
            dna_l = f.readline().rstrip().split()
            start = int(dna_l[0])
            end = int(dna_l[1])
            dna = dna_l[2]
            dnas.append((dna, start, end))

    t1 = time.time()

    trie = ACTrie()
    # genes_set = set(genes)
    trie.build(patterns=genes)

    print('after build tree', time.time() - t1)
    exit(0)

    for (dna, start, end) in dnas:

        # print('Start', dna)
        combine = defaultdict(int)
        for g, h in zip(genes[start: end + 1], health[start: end + 1]):
            combine[g] += h
        # print(combine)
        matches = trie.find_matching(dna)
        # print(dna, matches)
        h_total = 0

        for match in matches:
            h_total += combine[match]

        if min_ is None:
            min_ = h_total
        else:
            if h_total < min_:
                min_ = h_total

        if max_ is None:
            max_ = h_total
        else:
            if h_total > max_:
                max_ = h_total

    print(min_, max_)
    print(time.time()-t1)
