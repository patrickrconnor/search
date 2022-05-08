from re import U
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys

STOP_WORDS = set(stopwords.words("english"))


def remove_stop_stem(self, word: str):
    stemmer = PorterStemmer()
    if word not in STOP_WORDS:
        return stemmer.stem(word)


if __name__ == "__main__":
    arguments_number = len(sys.argv)
    if arguments_number == 5 or arguments_number == 4:
        all_words_regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
        use_pagerank = sys.argv[1] == "--pagerank"
        user_input = input("search>")
        while user_input != ":quit":
            input_list = [
                remove_stop_stem(x)
                for x in re.findall(all_words_regex, user_input)
            ]
            ##Score documents using the word Index, term to relevance dictionary,
            # then sort the second dictionary by relevance somehow (or create new data structure)
            # What is query term is not in corpus

    else:
        print(
            "The input should be of the form query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>"
        )
