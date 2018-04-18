import trie_node as TrieNode

class LevenshteinDistance:
    def __init__(self):
        self.Trie = TrieNode.TrieNode()

    def create_trie(self, file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            content = f.read().split('\n')
            for line in content:
                for word in line.split(', '):
                    self.Trie.insert(word)

    def search(self, word, max_cost):
        current_row = range(len(word) + 1)
        results = []
        for letter in self.Trie.children:
            self.__search_recursive(self.Trie.children[letter], letter, word, current_row, results, max_cost)
        return results

    def __search_recursive(self, node, letter, word, previous_row, results, max_cost):
        columns = len(word) + 1
        current_row = [previous_row[0] + 1]

        for column in range(1, columns):
            insert_cost = current_row[column - 1] + 1
            delete_cost = previous_row[column] + 1
            if word[column - 1] != letter:
                replace_cost = previous_row[column - 1] + 1
            else:
                replace_cost = previous_row[column - 1]
            current_row.append(min(insert_cost, delete_cost, replace_cost))

        if current_row[-1] <= max_cost and node.word is not None:
            results.append((node.word, current_row[-1]))

        if min(current_row) <= max_cost:
            for letter in node.children:
                self.__search_recursive(node.children[letter], letter, word, current_row, results, max_cost)