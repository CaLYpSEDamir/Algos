from queue import Queue
from collections import deque


class ACTrie:
    """Aho Corasick Trie"""

    def __init__(self):
        self.root = Node(output='')
        # self.q = Queue()
        self.q = deque()

    def _build(self, patterns):

        for w_i, word in enumerate(patterns):
            node = self.root
            for i, letter in enumerate(word, start=1):
                # output = (word, w_i) if i == len(word) else None
                output = word if i == len(word) else None
                node = node.append_letter(letter, output)

    def print(self, node):
        """"""
        print(node)
        for child in node.c.values():
            self.print(child)

    def _build_fails(self):
        """"""
        # root children to queue
        q = self.q
        for child in self.root.c.values():
            child.f = self.root
            # q.put(child)
            q.append(child)

        # while not q.empty():
        while len(q):
            # current = q.get()
            current = q.popleft()

            for letter, child in current.c.items():
                # q.put(child)
                q.append(child)

                # find a fail for child
                fail_node = current.f

                while True:
                    # fail_node has an appropriate letter
                    if letter in fail_node.c:
                        child.f = fail_node.c[letter]
                        child.o.extend(child.f.o)
                        break

                    # does not have letter
                    # if root
                    if fail_node.f is None:
                        child.f = fail_node
                        break
                    else:
                        # go to upper fail node
                        fail_node = fail_node.f

    def build(self, patterns):
        """"""
        self._build(patterns)
        self._build_fails()

    # fixme maybe as generator
    def find_matching(self, string):
        """"""
        # from collections import Counter
        # result = Counter()
        result = []
        current = self.root

        for letter in string:
            if letter in current.c:
                current = current.c[letter]
                result.extend(current.o)
                # result.update(current.o)

            # fixme here we need to check all fails up to root
            else:
                current = current.f
                while current is not None and letter not in current.c:
                    current = current.f
                # went up to root
                if current is None:
                    current = self.root
                    continue

                current = current.c[letter]
                result.extend(current.o)
                # result.update(current.o)

        return result
        # return set(result)
        # from collections import Counter
        # return Counter(result)


class Node:

    __slots__ = ('o', 'c', 'f')

    def __init__(self, output=None):

        self.o = []
        self.c = {}
        self.f = None

        if output:
            self.o.append(output)

    def __str__(self):
        return f'Node: ' \
               f'outputs: `{self.o}` ' \
               f'fail_node: {getattr(self.f, "letter", None)}'

    def append_letter(self, letter, output=None) -> 'Node':

        if letter in self.c:
            child = self.c[letter]
            if output:
                child.o.append(output)
        else:
            child = Node(output=output or None)
            self.c[letter] = child

        return child


if __name__ == '__main__':


    # words = ['asd', 'as', 'a', 'bdd']
    # words = ['c', 'cc', 'ccc', 'cccc']
    # words = []
    words = ['aab', 'aab']
    # words = ['c', 'dadac']
    # words = ['a', 'ab', 'bc', 'aab', 'aac', 'bd']

    trie = ACTrie()
    trie.build(patterns=words)
    trie.print(trie.root)

    # string = 'aaab'
    # string = 'abcabcabc'
    string = 'bcaab'

    matches = trie.find_matching(string)
    print(matches)
