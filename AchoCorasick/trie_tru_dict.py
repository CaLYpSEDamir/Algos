from queue import Queue


class ACTrie:
    """Aho Corasick Trie"""

    def __init__(self):
        self.root = Node(output='')
        self.q = Queue()

    def _build(self, patterns):

        for word in patterns:
            node = self.root
            for i, letter in enumerate(word, start=1):
                output = word if i == len(word) else None
                node = node.append_letter(letter, output)

    def print(self, node):
        """"""
        print(node)
        for child in node.children.values():
            self.print(child)

    def _build_fails(self):
        """"""
        # root children to queue
        for child in self.root.children.values():
            child.fail_node = self.root
            self.q.put(child)

        while not self.q.empty():
            current = self.q.get()

            for letter, child in current.children.items():
                self.q.put(child)
                # find a fail for child
                fail_node = current.fail_node

                while True:
                    # fail_node has an appropriate letter
                    if letter in fail_node.children:
                        child.fail_node = fail_node.children[letter]
                        child.outputs.extend(child.fail_node.outputs)
                        break

                    # does not have letter
                    # if root
                    if fail_node.fail_node is None:
                        child.fail_node = fail_node
                        break
                    else:
                        # go to upper fail node
                        fail_node = fail_node.fail_node

    def build(self, patterns):
        """"""
        self._build(patterns)
        self._build_fails()

    def find_matching(self, string):
        """"""
        result = []
        current = self.root

        for letter in string:
            if letter in current.children:
                current = current.children[letter]
                result.extend(current.outputs)

            # fixme here we need to check all fails up to root
            else:
                current = current.fail_node
                while current is not None and letter not in current.children:
                    current = current.fail_node
                # went up to root
                if current is None:
                    current = self.root
                    continue

                current = current.children[letter]
                result.extend(current.outputs)

        return result


class Node:

    __slots__ = ('outputs', 'children', 'fail_node')

    def __init__(self, output=None):

        self.outputs = []
        self.children = {}
        self.fail_node = None

        if output:
            self.outputs.append(output)

    # def __str__(self):
    #     return f'Node: ' \
    #            f'outputs: `{self.outputs}` ' \
    #            f'fail_node: {getattr(self.fail_node, "letter", None)}'

    def append_letter(self, letter, output=None) -> 'Node':

        if letter in self.children:
            child = self.children[letter]
            if output:
                child.outputs.append(output)
        else:
            child = Node(output=output or None)
            self.children[letter] = child

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
