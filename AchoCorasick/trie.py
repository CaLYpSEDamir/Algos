from queue import Queue


class ACTrie:
    """Aho Corasick Trie"""

    def __init__(self, root):
        self.root = root
        self.q = Queue()

    def _build(self, words):

        for word in words:
            node = self.root
            for i, letter in enumerate(word, start=1):
                is_word = i == len(word)
                output = word[:i]
                node = node.append_letter(letter, is_word, output)

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

            for child in current.children.values():
                self.q.put(child)
                # find a fail for child
                fail_node = current.fail_node

                while True:
                    # fail_node has an appropriate letter
                    if child.letter in fail_node.children:
                        child.fail_node = fail_node.children[child.letter]
                        child.outputs.extend(child.fail_node.outputs)
                        break

                    # does not have letter
                    # if root
                    if fail_node.is_root():
                        child.fail_node = fail_node
                        break
                    else:
                        # go to upper fail node
                        fail_node = fail_node.fail_node

    def _find_matching(self, string):
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
                # went up to rrot
                if current is None:
                    current = self.root
                    continue

                current = current.children[letter]
                result.extend(current.outputs)

        return result

    def _find_matching2(self, string):
        """"""
        result = []
        current = self.root

        for letter in string:
            # print(80 * '-')
            # print(f'Started {letter}')
            while current is not None and letter not in current.children:
                print('in while')
                current = current.fail_node
            if current is None:
                # print('node is None')
                current = self.root
                continue
            # print(f'{current}')
            current = current.children[letter]
            # print(f'{current}')
            result.extend(current.outputs)
        return result


class Node:

    def __init__(self, level, letter, is_word, output=None):

        self.level = level
        self.letter = letter
        self.outputs = []
        self.is_word = is_word
        self.children = {}
        self.fail_node = None

        if output:
            self.outputs.append(output)

    def __str__(self):
        return f'Node: letter: `{self.letter}` ' \
               f'outputs: `{self.outputs}` ' \
               f'fail_node: {getattr(self.fail_node, "letter", None)}'

    def is_root(self):
        return self.letter == ''

    def append_letter(self, letter, is_word=False, output=None) -> 'Node':

        if letter in self.children:
            child = self.children[letter]
            if is_word:
                child.is_word = True
                child.outputs.append(output)
        else:
            child = Node(level=self.level+1, letter=letter, is_word=is_word, output=output if is_word else None)
            self.children[letter] = child

        return child


if __name__ == '__main__':

    root = Node(level=0, letter='', is_word=False, output='')
    trie = ACTrie(root=root)

    # words = ['asd', 'as', 'a', 'bdd']
    # words = ['c', 'cc', 'ccc', 'cccc']
    # words = []
    # words = ['aab']
    # words = ['c', 'dadac']
    words = ['a', 'ab', 'bc', 'aab', 'aac', 'bd']

    trie._build(words=words)
    trie._build_fails()
    trie.print(trie.root)

    # string = 'aaab'
    # string = 'abcabcabc'
    string = 'bcaab'

    matches = trie._find_matching(string)
    # matches = trie._find_matching2(string)
    print(matches)
