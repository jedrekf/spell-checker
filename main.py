import time
import sys

from levenshtein_distance import LevenshteinDistance

def main(argv):

    ld = LevenshteinDistance()

    ld.create_trie('./korpus.txt')

    start = time.time()
    results = ld.search('przejąc', 1)
    end = time.time()

    for result in results:
        print(result)

    print("Search took %g s" % (end - start))

main(sys.argv[1:])
