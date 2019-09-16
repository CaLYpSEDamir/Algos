import os
import re
import sys
import math
import random
from collections import defaultdict

from .trie import ACTrie


if __name__ == '__main__':
    n = int(input())
    genes = input().rstrip().split()
    health = list(map(int, input().rstrip().split()))

    s = int(input())

    trie = ACTrie()
    genes_set = set(genes)
    trie.build(patterns=genes_set)
    min_ = None
    max_ = None

    for s_itr in range(s):
        firstLastd = input().split()
        start = int(firstLastd[0])
        end = int(firstLastd[1])
        dna = firstLastd[2]

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
