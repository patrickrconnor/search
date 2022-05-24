from re import U
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys

from pyparsing import empty
import file_io

STOP_WORDS = set(stopwords.words("english"))
ids_to_titles: dict[int:str] = {}
words_ids_relevance: dict[str : dict[int:float]] = {}
ids_ranks: dict[int:float] = {}
id_score: dict[int:float] = {}


def read_arguments():
    arguments_number = len(sys.argv)
    use_pagerank = False
    if arguments_number == 5 or arguments_number == 4:
        use_pagerank = sys.argv[1] == "--pagerank"
        if use_pagerank:
            file_io.read_title_file(sys.argv[2], ids_to_titles)
            file_io.read_docs_file(sys.argv[3], ids_ranks)
            file_io.read_words_file(sys.argv[4], words_ids_relevance)
        else:
            file_io.read_title_file(sys.argv[1], ids_to_titles)
            file_io.read_words_file(sys.argv[3], words_ids_relevance)
    else:
        print(
            "The input should be of the form query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>"
        )
    return use_pagerank


def remove_stop_stem(word: str):
    stemmer = PorterStemmer()
    if word not in STOP_WORDS:
        return stemmer.stem(word)


def score(input_list):
    use_pagerank = read_arguments()
    for input_word in input_list:
        if input_word in words_ids_relevance:
            for (k, v) in words_ids_relevance[input_word].items():
                if k in id_score:
                    id_score[k] += v
                else:
                    id_score[k] = v
    if use_pagerank:
        for (k, v) in id_score.items():
            id_score[k] *= ids_ranks[k]


if __name__ == "__main__":
    all_words_regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
    user_input = input("search>")
    while user_input != ":quit":
        input_list = [
            remove_stop_stem(x) for x in re.findall(all_words_regex, user_input)
        ]
        score(input_list)
        if id_score == {}:
            print("None of the words in the query appear in the wiki")
            continue
        output_list = sorted(id_score, key=id_score.get)
        for i in range(10):
            print(f"{i+1} {output_list[i]}")
