#!/usr/bin/env python
import bisect
import sys


# -------------------------------------------------------------------------------

class Node(object):
    __slots__ = ['genes', 'h_sum', 'children']

    def __init__(self):
        self.genes = None
        self.h_sum = None
        self.children = {}

    def __repr__(self):
        return "< genes:%s h_sum:%s children:%s>" % (self.genes, self.h_sum, self.children)

    def __str__(self):
        return " genes is %s, h_sum is %s, children is %s" % (self.genes, self.h_sum, self.children)


# -------------------------------------------------------------------------------
# file = 'test_case_1823728075410_1823728075410.txt'
# file = 'test_case_runtime_error_0_8652768.txt'
file = 'Test2_15806635_20688978289.txt'
# file = 'simple_test.txt'

dnas = []

with open(file) as f:
    num_of_genes = f.readline()
    genes = f.readline().rstrip().split()
    health = list(map(int, f.readline().rstrip().split()))
    n = int(f.readline())

    for _ in range(n):
        dna_l = f.readline().rstrip().split()
        start = int(dna_l[0])
        end = int(dna_l[1])
        dna = dna_l[2]

        dnas.append((dna, start, end))

# -------------------------------------------------------------------------------
root = Node()

for gid, gene in enumerate(genes):
    node = root
    gene_len = len(gene)
    for i, c in enumerate(gene):
        if c in node.children:
            node = node.children[c]
        else:
            child = Node()
            node.children[c] = child
            node = child
        if i == gene_len - 1:
            if node.genes is None:
                node.genes = []
                node.h_sum = []
            node.genes.append(gid)

L = [root]
while L:
    node = L.pop()
    if not node.genes is None:
        node.genes.sort()
        node.h_sum = [0] * (len(node.genes) + 1)
        for idx, gid in enumerate(node.genes):
            node.h_sum[idx + 1] = node.h_sum[idx] + health[gid]

    for child in node.children.values():
        L.append(child)


# -------------------------------------------------------------------------------
def get_health(seq, first, last):
    seq_len = len(seq)

    h_tot = 0

    L = []
    for idx, c in enumerate(seq):
        if not c in root.children: continue
        L.append(idx)
    for idx in L:
        node, pos = root, idx
        while node and pos < seq_len:
            c = seq[pos]

            child = node.children.get(c, None)
            if child and child.genes:
                lb = bisect.bisect_left(child.genes, first)
                ub = bisect.bisect(child.genes, last, lo=lb)
                h_tot += child.h_sum[ub] - child.h_sum[lb]

            node = child
            pos += 1

    return h_tot


# -------------------------------------------------------------------------------
h_tot_min = sys.maxsize
h_tot_max = 0

f_min = num_of_genes
f_max = 0

# for a0 in range(s):
#     first, last, d = input().strip().split(' ')
#     first, last, d = [int(first), int(last), str(d)]

# print(dnas)
for (d, first, last) in dnas[:]:

    h_tot = get_health(d, first, last)

    h_tot_min = min(h_tot_min, h_tot)
    h_tot_max = max(h_tot_max, h_tot)

print(h_tot_min, h_tot_max)
