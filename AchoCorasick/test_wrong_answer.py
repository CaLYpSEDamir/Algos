import os
import re
import sys
import time
import math
import random
from collections import defaultdict, Counter

from memory_profiler import profile

from trie import ACTrie


# @profile
def go():
    # file = 'test_case_1823728075410_1823728075410.txt'
    # file = 'test_case_runtime_error_0_8652768.txt'
    file = 'Test2_15806635_20688978289.txt'

    dnas = []
    pure_dnas = set()
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

    print('dnas', len(dnas))
    # exit(0)
    # return

    # dnas = set(dnas)

    for i, (dna, start, end) in enumerate(dnas[:1000]):
        # print()
        # if i == 1000:
        #     break
        # print('Start', dna)

        combine = defaultdict(int)
        for g, h in zip(genes[start: end + 1], health[start: end + 1]):
            combine[g] += h

        # for j in range(start, end + 1):
        #     combine[genes[j]] += health[j]

        # combine = Counter()
        # for j in range(start, end + 1):
        #     combine[genes[j]] += health[j]

        # print(combine)
        matches = trie.find_matching(dna)
        # print(len(matches))

        # h_total = 0
        # for match in matches:
        #     h_total += combine[match]
        #
        # c: Counter = trie.find_matching(dna)
        # for k in c:
        #     h_total += combine[k] * c[k]

        # if min_ is None:
        #     min_ = h_total
        # else:
        #     if h_total < min_:
        #         min_ = h_total
        #
        # if max_ is None:
        #     max_ = h_total
        # else:
        #     if h_total > max_:
        #         max_ = h_total

    print(min_, max_)

    print(time.time()-t1)


if __name__ == '__main__':
    go()
