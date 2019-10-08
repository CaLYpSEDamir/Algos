import os
import re
import sys
import time
import math
import bisect
from collections import defaultdict, Counter

from memory_profiler import profile

from trie import ACTrie


# @profile
def go():
    # file = 'test_case_1823728075410_1823728075410.txt'
    # file = 'test_case_runtime_error_0_8652768.txt'
    file = 'Test2_15806635_20688978289.txt'

    dnas = []
    dna_indexes = defaultdict(list)
    dna_healths = defaultdict(lambda: [0])
    # dna_healths = defaultdict(list)
    min_ = None
    max_ = None

    with open(file) as f:
        n = f.readline()
        genes = f.readline().rstrip().split()
        all_healths = list(map(int, f.readline().rstrip().split()))

        words_cnt = int(f.readline())

        for _ in range(words_cnt):
            dna_l = f.readline().rstrip().split()
            start = int(dna_l[0])
            end = int(dna_l[1])
            dna = dna_l[2]
            dnas.append((dna, start, end))

    t1 = time.time()

    trie = ACTrie()
    genes_c = Counter(genes)

    for i, gen in enumerate(genes):
        dna_indexes[gen].append(i)
        dna_healths[gen].append(dna_healths[gen][-1] + all_healths[i])

    trie.build(patterns=set(genes))

    print('after build tree', time.time() - t1)

    print('dnas', len(dnas))
    # exit(0)
    # return

    # dnas = set(dnas)

    all_time = 0

    for i, (dna, start, end) in enumerate(dnas[:100000]):

        h_total = 0
        matches = trie.find_matching(dna)

        for m in matches:



        ##########################

        cache_indexes = dict()

        for m in matches:

            if m not in cache_indexes:
                to_add = 0
                st = bisect.bisect_left(dna_indexes[m], start)
                en = bisect.bisect_left(dna_indexes[m], end)

                tt = time.time()
                for j in dna_indexes[m][st:en]:
                # for j in dna_indexes[m]:
                    # print(m, dna_indexes[m])
                    # if start <= j <= end+1:
                    #     to_add += genes_c[m] * health[j]
                    to_add += genes_c[m] * all_healths[j]

                ttt = time.time()
                all_time += (ttt -tt)

                cache_indexes[m] = to_add
                h_total += to_add
            else:
                # print('hit')
                h_total += cache_indexes[m]

                # for g, h in zip(genes[start: end + 1], health[start: end + 1]):
        #     for m in matches:
        #         if m == g:
        #             h_total += h * genes_c[m]
        # print(len(matches))

        # h_total = 0
        # for match in matches:
        #     h_total += combine[match]
        #
        # c: Counter = trie.find_matching(dna)
        # for k in c:
        #     h_total += combine[k] * c[k]

        # fixme refactor
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
    print(all_time)

    print(time.time()-t1)


if __name__ == '__main__':
    go()
