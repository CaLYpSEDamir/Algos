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
    file = 'Test31_1823728075410_1823728075410.txt'
    # file = 'test_case_runtime_error_0_8652768.txt'
    # file = 'Test2_15806635_20688978289.txt'
    # file = 'simple_test.txt'
    #
    dnas = []
    dna_indexes = defaultdict(list)
    dna_healths = defaultdict(list)
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
    trie.build(patterns=set(genes))

    for i, gen in enumerate(genes):

        dna_indexes[gen].append(i)

        if not dna_healths[gen]:
            dna_healths[gen].append(all_healths[i])
        else:
            dna_healths[gen].append(dna_healths[gen][-1] + all_healths[i])

    # trie.build(patterns=genes)

    # print('after build tree', time.time() - t1)

    # print('dnas', len(dnas))
    # exit(0)
    # return

    # dnas = set(dnas)

    all_time = 0

    for i, (dna, start, end) in enumerate(dnas[:]):
        # print(i, dna, start, end)
        # print(i)

        h_total = 0
        matches = trie.find_matching(dna)

        # print(matches)
        # print(set(matches))

        cache_indexes = dict()

        for m in matches:

            to_add = 0

            m_list = dna_indexes[m]

            # print('m_list', m_list)
            len_m_list = len(m_list)

            end_id = bisect.bisect_left(m_list, end)

            # l([0, 5], 6) -> 2
            # вышли за правый предел
            if end_id == len_m_list:
                end_id -= 1
            # индекса end нет, но есть больше него

            elif end < m_list[end_id]:
                end_id -= 1

            # иначе l([0, 6], 6) -> 1 оставим как есть


            start_id = bisect.bisect_left(m_list, start)
            # print(m_list)
            # break

            first = m_list[0]
            last = m_list[-1]
            # вышли за границу r([0,4], 5)
            if start > last or first > end:
                # print(f'Skipping1')
                # print(80 * '-')
                continue
            # print('start_id left', start_id)

            # l([0,1,5], 0) -> 0
            if start_id == 0:
                h_total += dna_healths[m][end_id]

                # print(f'Skipping2', h_total)
                continue
            # совпадение l([0,1,5], 1) -> 1, возьмем предыдущее
            if start == m_list[start_id]:
                start_id -= 1
            # нет элемента, l([0,3,5], 1) -> 1, возьмем предыдущее
            elif start < m_list[start_id]:
                start_id -= 1

            to_add += dna_healths[m][end_id] - dna_healths[m][start_id]

            h_total += to_add

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

    print(time.time() - t1)


if __name__ == '__main__':
    go()
