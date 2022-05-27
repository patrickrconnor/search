from re import U
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys

from pyparsing import empty
import file_io

# store a set of stopwords
STOP_WORDS = set(stopwords.words("english"))
# Store a set of global variables corresponding to the data structures needed for
# querying
ids_to_titles: dict[int:str] = {}
words_ids_relevance: dict[str : dict[int:float]] = {}
ids_ranks: dict[int:float] = {}
id_score: dict[int:float] = {}


def read_arguments():
    """Reads user input and stores it appropriately in the corresponding
    dictionaries

    Returns:
    A boolean representing wether --pagerank was detected in user input"""
    # Store the number of arguments
    arguments_number = len(sys.argv)
    # Intatiate pagerank as false
    use_pagerank = False
    # Check that input is expected length
    if arguments_number == 5 or arguments_number == 4:
        # Check if the first term in input is --pagerank and update boolean
        # appropriately
        use_pagerank = sys.argv[1] == "--pagerank"
        # Read in input from files into corresponding dictionaries, adjusting for
        # pagerank
        if use_pagerank:
            file_io.read_title_file(sys.argv[2], ids_to_titles)
            file_io.read_docs_file(sys.argv[3], ids_ranks)
            file_io.read_words_file(sys.argv[4], words_ids_relevance)
        else:
            file_io.read_title_file(sys.argv[1], ids_to_titles)
            file_io.read_words_file(sys.argv[3], words_ids_relevance)
    else:
        print(
            "The input should be of the form query.py [--pagerank] <titleIndex> \
            <documentIndex> <wordIndex>"
        )
    return use_pagerank


def score(input_list):
    """Fills a page id to score dictionary based on an input query
    Parameters:
    input_list - a list of all the words of the user input query,
    tokenized and stemmed
    Side Effects:
    Populates an id to score dictionary with the score each page id has for the
    query"""
    # Store a boolean representing wether pagerank should be used
    use_pagerank = read_arguments()
    # Loop through each word and sum all the relevance for each page in which
    # each word in the query appears
    for input_word in input_list:
        if input_word in words_ids_relevance:
            for (k, v) in words_ids_relevance[input_word].items():
                if k in id_score:
                    id_score[k] += v
                else:
                    id_score[k] = v
    # If pagerank is being used multiply each score by the corresponding rank
    if use_pagerank:
        for (k, v) in id_score.items():
            id_score[k] *= ids_ranks[k]


# This is the main method that runs the program
if __name__ == "__main__":
    stemmer = PorterStemmer()
    all_words_regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
    # Prompt the user for input
    user_input = input("search>")
    # Use a while loop to continue prompting the user for input unitl :quit is
    # typed
    while user_input != ":quit":
        # Tokenize and stem, user input
        input_list = [
            stemmer.stem(x)
            for x in re.findall(all_words_regex, user_input)
            if x not in STOP_WORDS
        ]
        # Call score to score pages based on input
        score(input_list)
        # check if no documents match query
        if id_score == {}:
            print("None of the words in the query appear in the wiki")
            # Re-prompt user
            user_input = input("search>")
            # Don't execute the rest of the loop
            continue
        # Store the output list sorted from highest score to lowest
        output_list = sorted(id_score, key=id_score.get, reverse=True)
        # Print out_put list appropriately
        if len(output_list) < 10:
            for i in range(len(output_list)):
                print(f"{i+1} {ids_to_titles[output_list[i]]}")
        else:
            for i in range(10):
                print(f"{i+1} {ids_to_titles[output_list[i]]}")
        # Clear id_score dictionary for next query
        id_score = {}
        # Re-prompt user
        user_input = input("search>")
