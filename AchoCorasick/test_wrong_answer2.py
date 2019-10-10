import os
import re
import sys
import time
import math
import bisect
from collections import defaultdict, Counter

# from memory_profiler import profile

from trie import ACTrie


# @profile
def go():
    # file = 'test_case_1823728075410_1823728075410.txt'
    # file = 'test_case_runtime_error_0_8652768.txt'
    file = 'Test2_15806635_20688978289.txt'
    # file = 'simple_test.txt'

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

    # trie.build(patterns=set(genes))
    trie.build(patterns=genes)

    print('after build tree', time.time() - t1)

    print('dnas', len(dnas))
    # exit(0)
    # return

    # dnas = set(dnas)

    all_time = 0

    for i, (dna, start, end) in enumerate(dnas[:1000]):
        # print(i, dna, start, end)
        # print(i)

        h_total = 0
        matches = trie.find_matching(dna)

        # print(matches)

        cache_indexes = dict()

        for (m, ind) in matches:
            print('m', m, ind)
            # if m in cache_indexes:
            #     h_total += all_healths[ind]

            if start <= ind <= end:

                h_total += all_healths[ind]

        # print(h_total)
        # h_total = 0

        # for m, ind in matches:
        #     print('m', m)
        #     # if m not in cache_indexes:
        #     if 1:
        #
        #         m_list = dna_indexes[m]
        #         # print('m_list', m_list)
        #         len_m_list = len(m_list)
        #
        #         end_id = bisect.bisect_left(dna_indexes[m], end)
        #
        #         # l([5], 6) -> 1
        #         if end_id == len_m_list:
        #             end_id -= 1
        #         else:
        #             # l([5, 6], 6) -> 1 - normal
        #
        #             e = m_list[end_id]
        #
        #             if e != end:
        #                 # l([7], 6) -> 0
        #                 if end_id == 0:
        #                     print('Skipping')
        #                     continue
        #                 # l([5], 6) -> 1
        #                 end_id -= 1
        #
        #         start_id = bisect.bisect_left(dna_indexes[m], end)
        #
        #         # l([1], 2) -> 1
        #         if start_id == len_m_list:
        #             start_id -= 1
        #         else:
        #             # l([2, 3], 2) -> 0 - normal
        #
        #             s = m_list[start_id]
        #
        #             if s != start:
        #                 # l([7], 6) -> 0
        #                 if start_id == 0:
        #                     print('Skipping')
        #                     continue
        #                 # l([5], 6) -> 1
        #                 start_id -= 1
        #
        #         to_add = 0
        #
        #         # tt = time.time()
        #
        #         to_add += all_healths[end_id] - all_healths[start_id]
        #
        #         ttt = time.time()
        #         all_time += (ttt -tt)
        #
        #         cache_indexes[m] = to_add
        #         h_total += to_add
        #     else:
        #         print('hit cache')
        #         h_total += cache_indexes[m]

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
