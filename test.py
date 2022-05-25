import pytest

from file_io import *
from index import *

# You should test the calculations computed by your search engine using pytest assertions.
# This includes the calculations from the Indexer as well as expected TF and IDF calculations and PageRank calculations.
# You should also test that you are parsing, tokenizing, etc the documents and queries in the expected manner.

# -----------------------------------------------------------------------
# Parse
# -----------------------------------------------------------------------

# INDIVIDUAL PARSE COMPONENTS:


def test_extract_title():
    pass


def test_extract_id():
    pass


def test_extract_text():
    pass


def test_tokenize_and_stem():
    # tokenize, stem, and remove stop words
    indexer_0 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/simple_wiki_0.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    test_string_input_0 = ""
    test_list_output_0 = [""]
    assert (
        indexer_0.tokenize_and_stem(test_string_input_0) == test_list_output_0
    )

    test_string_input_1 = "crayola"
    test_list_output_1 = ["crayola"]
    assert (
        indexer_0.tokenize_and_stem(test_string_input_1) == test_list_output_1
    )

    test_string_input_2 = (
        "make a phone call tonight and begin calling cousins and siblings"
    )
    test_list_output_2 = [
        "make",
        "phone",
        "call",
        "tonight",
        "begin",
        "call",
        "cousin",
        "sibling",
    ]
    assert (
        indexer_0.tokenize_and_stem(test_string_input_2) == test_list_output_2
    )

    test_string_input_3 = (
        "cars automobiles trains running and kayaking or swims"
    )
    test_list_output_3 = ["car", "automobile", "train", "run", "kayak", "swim"]
    assert (
        indexer_0.tokenize_and_stem(test_string_input_3) == test_list_output_3
    )


def test_remove_stop_stem():
    indexer_0 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/simple_wiki_0.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    # checking for stop word remover functionality
    assert indexer_0.remove_stop_stem("") == ""
    assert indexer_0.remove_stop_stem("and") == ""
    assert indexer_0.remove_stop_stem("or") == ""
    assert indexer_0.remove_stop_stem("if") == ""  # is this one

    # checking for stemmer functionality
    assert indexer_0.remove_stop_stem("hold") == "hold"
    assert indexer_0.remove_stop_stem("artery") == "arter"  # "artery"?
    assert indexer_0.remove_stop_stem("arteries") == "arter"
    assert indexer_0.remove_stop_stem("keys") == "key"
    assert indexer_0.remove_stop_stem("keying") == "key"
    assert indexer_0.remove_stop_stem("keyed") == "key"


def test_euclidean_distance():
    indexer_page_rank_example_1 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/PageRankExample1.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    test_dict_iteration_0 = {1: 0.3333, 2: 0.3333, 3: 0.3333}

    test_dict_iteration_1 = {1: 0.4750, 2: 0.1916, 3: 0.3333}

    test_dict_iteration_2 = {1: 0.4148, 2: 0.2519, 3: 0.3333}

    test_dict_iteration_3 = {1: 0.4404, 2: 0.2263, 3: 0.3333}

    test_dict_iteration_4 = {1: 0.4295, 2: 0.2272, 3: 0.3333}

    test_dict_iteration_5 = {1: 0.4341, 2: 0.2325, 3: 0.3333}

    test_dict_iteration_6 = {1: 0.4322, 2: 0.2345, 3: 0.3333}

    test_dict_iteration_7 = {1: 0.4330, 2: 0.2337, 3: 0.3333}

    test_dict_iteration_8 = {1: 0.4326, 2: 0.2340, 3: 0.3333}

    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_0, test_dict_iteration_1
        )
        == 0.2003
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_1, test_dict_iteration_2
        )
        == 0.0851
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_2, test_dict_iteration_3
        )
        == 0.0362
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_3, test_dict_iteration_4
        )
        == 0.0154
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_4, test_dict_iteration_5
        )
        == 0.0065
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_5, test_dict_iteration_6
        )
        == 0.0028
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_6, test_dict_iteration_7
        )
        == 0.0012
    )
    assert (
        indexer_page_rank_example_1.euclidean_distance(
            test_dict_iteration_7, test_dict_iteration_8
        )
        == 0.0005
    )


def test_weight():
    indexer_page_rank_example_1 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/PageRankExample1.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    # page links: dict of (id of doc) -> (set of ids linked to by doc)

    # list of pages in PageRankExample1:
    # id 1: A
    # id 2: B
    # id 3: C
    assert indexer_page_rank_example_1.weight(1, 2) == 0.475
    assert indexer_page_rank_example_1.weight(1, 3) == 0.475
    assert indexer_page_rank_example_1.weight(2, 1) == 0.475
    assert indexer_page_rank_example_1.weight(2, 3) == 0.475

    assert indexer_page_rank_example_1.weight(3, 1) == 0.09

    assert indexer_page_rank_example_1.weight(1, 1) == 0.05
    assert indexer_page_rank_example_1.weight(2, 2) == 0.05
    assert indexer_page_rank_example_1.weight(3, 3) == 0.05
    assert indexer_page_rank_example_1.weight(3, 2) == 0.05


def test_calculate_t_f():  # is tf testing already covered by one of the dictionaries written to in the parse testing
    pass


def test_calculate_idf():  # same as tf?
    pass


# -------------------------------------------------------------------------


def test_indexer_parse():

    # simple_wiki_0 test cases
    indexer_0 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/simple_wiki_0.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_0.parse()
    assert indexer_0.ids_to_titles.get(0) == "Soda"
    assert indexer_0.titles_to_ids.get("Soda") == 0

    # for the word soda in document with id 0, does it appear 1 times
    assert indexer_0.words_ids_counts.get("soda").get(0) == 1

    # tf for soda in document 0 = 1
    # idf = log(1/1) = 0
    assert indexer_0.words_ids_relevance.get("soda").get(0) == 0

    # assert indexer_0.parse(
    #     "/Users/satchwaldman/Desktop/cs0200/projects/ \
    #     search-PVIP35-satchwaldman/simple_wiki_0.xml") == "soda"

    # -----------------------------------------------------------------------

    indexer_1 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/simple_wiki_1.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    # assert indexer_1.parse(
    #     "/Users/satchwaldman/Desktop/cs0200/projects/ \
    #     search-PVIP35-satchwaldman/simple_wiki_1.xml") \
    #         == "Cars are sometimes known as automobiles \
    #             This is a delicious sauce used for dipping"

    # -----------------------------------------------------------------------
    # Page Rank
    # -----------------------------------------------------------------------

    # *** Does Page Rank make sense without a query? Can we just standalone
    #     test it like this?

    # NOTE: everything here indexes at 1


def test_indexer_page_rank():
    # Expected: Rank(A) = 0.4326, Rank(B) = 0.2340, Rank(C) = 0.3333
    indexer_page_rank_1 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/PageRankExample1.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_page_rank_1.page_rank()
    # is it correct to treat node A as id 1, etc (according to xml)
    assert abs(indexer_page_rank_1.ids_ranks.get(1) - 0.4326) <= 0.0001
    assert (
        abs(indexer_page_rank_1.ids_ranks.get(2) - 0.2340) <= 0.0001
    )  # should we do this? (checking if value is within some error)
    assert abs(indexer_page_rank_1.ids_ranks.get(3) - 0.3333) <= 0.0001

    assert indexer_page_rank_1.page_most_common_apppearances.get(1) == 1
    # second doc has no text (should we test this?)
    assert indexer_page_rank_1.page_most_common_apppearances.get(3) == 1

    # assert indexer_page_rank_1.page_links.get(0) == 2
    # assert indexer_page_rank_1.page_links.get(1) == 0 # is this correct to do?
    # assert indexer_page_rank_1.page_links.get(2) == 1

    assert 2 in indexer_page_rank_1.page_links.get(1)
    assert 3 in indexer_page_rank_1.page_links.get(1)

    # nothing in .get(2)

    assert 1 in indexer_page_rank_1.page_links.get(3)

    # -----------------------------------------------------------------------

    # Expected: Rank(A) = 0.2018, Rank(B) = 0.0375, Rank(C) = 0.3740, Rank(D) = 0.3867
    indexer_page_rank_2 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/PageRankExample2.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_page_rank_2.page_rank()

    assert indexer_page_rank_2.ids_ranks.get(1) == 0.2018
    assert indexer_page_rank_2.ids_ranks.get(2) == 0.0375
    assert indexer_page_rank_2.ids_ranks.get(3) == 0.3740
    assert indexer_page_rank_2.ids_ranks.get(4) == 0.3867

    assert indexer_page_rank_2.page_most_common_apppearances.get(1) == 1
    assert indexer_page_rank_2.page_most_common_apppearances.get(2) == 1
    assert indexer_page_rank_2.page_most_common_apppearances.get(3) == 1
    assert indexer_page_rank_2.page_most_common_apppearances.get(4) == 1

    assert 3 in indexer_page_rank_2.page_links.get(1)

    assert 4 in indexer_page_rank_2.page_links.get(2)

    assert 4 in indexer_page_rank_2.page_links.get(3)

    assert 1 in indexer_page_rank_2.page_links.get(4)
    assert 3 in indexer_page_rank_2.page_links.get(4)

    # -----------------------------------------------------------------------

    # Expected: Rank(A) = 0.0524, Rank(B) = 0.0524, Rank(C) = 0.4476, Rank(D) = 0.4476
    indexer_page_rank_3 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/PageRankExample3.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_page_rank_3.page_rank()

    assert indexer_page_rank_3.ids_ranks.get(1) == 0.0524
    assert indexer_page_rank_3.ids_ranks.get(2) == 0.0524
    assert indexer_page_rank_3.ids_ranks.get(3) == 0.4476
    assert indexer_page_rank_3.ids_ranks.get(4) == 0.4476

    assert indexer_page_rank_3.page_most_common_apppearances.get(0) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(1) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(2) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(3) == 1

    assert 1 in indexer_page_rank_2.page_links.get(1)
    assert 2 in indexer_page_rank_2.page_links.get(2)
    assert 4 in indexer_page_rank_2.page_links.get(3)
    assert 3 in indexer_page_rank_2.page_links.get(4)

    # -----------------------------------------------------------------------

    # Expected: Rank(A) = 0.0375, Rank(B) = 0.0375, Rank(C) = 0.4625, Rank(D) = 0.4625
    indexer_page_rank_4 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/PageRankExample4.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_page_rank_4.page_rank()

    assert indexer_page_rank_4.ids_ranks.get(1) == 0.0375
    assert indexer_page_rank_4.ids_ranks.get(2) == 0.0375
    assert indexer_page_rank_4.ids_ranks.get(3) == 0.4625
    assert indexer_page_rank_4.ids_ranks.get(4) == 0.4625

    assert indexer_page_rank_3.page_most_common_apppearances.get(0) == 3
    assert indexer_page_rank_3.page_most_common_apppearances.get(1) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(2) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(3) == 2

    assert 3 in indexer_page_rank_2.page_links.get(1)
    assert 4 in indexer_page_rank_2.page_links.get(2)
    assert 4 in indexer_page_rank_2.page_links.get(3)
    assert 3 in indexer_page_rank_2.page_links.get(4)

    # -----------------------------------------------------------------------

    indexer_0 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/simple_wiki_0.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_0.page_rank()
    # computing PageRank with no edges (connections between pages)?
    assert indexer_0.ids_ranks.get(0) == 1  # is this correct for base case?
    assert indexer_0.page_most_common_apppearances.get(0) == 1  # only one word
    # doesn't make sense to test on the page_links dictionary because the values (set of links for each doc) is an empty set

    indexer_1 = Indexer(
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/simple_wiki_1.xml",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/titles.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/docs.txt",
        "/Users/satchwaldman/Desktop/cs0200/projects/search-PVIP35-satchwaldman/words.txt",
    )

    indexer_1.page_rank()
    # MANUAL PAGE RANK CALCS:
    # none of the pages in this wiki link to one another
    # still a useful base case
    assert (
        indexer_1.ids_ranks.get(0) == 0.5
    )  # both should be equal and sum to 1 because they (the docs) are not related?
    assert indexer_1.ids_ranks.get(1) == 0.5

    # a_j = max(i) (c_i_j) (how many term i in doc j)
    assert (
        indexer_1.page_most_common_apppearances.get(0) == 1
    )  # each word appears once
