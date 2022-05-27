from operator import index
import pytest

from file_io import *
from index import *

# You should test the calculations computed by your search engine using pytest assertions. 
# This includes the calculations from the Indexer as well as expected TF and IDF calculations and PageRank calculations.
# You should also test that you are parsing, tokenizing, etc the documents and queries in the expected manner.

# -----------------------------------------------------------------------
                                #Parse
# -----------------------------------------------------------------------

# INDIVIDUAL PARSE COMPONENTS:

def test_extract_title():
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_0.parse()


def test_extract_id():
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    
    #page_0 = <page> <title> Soda </title> <id> 1 </id> <text> soda </text> </page> 

    #assert indexer_0.extract_id(page_0) == 1

def test_extract_text():
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_0.parse()

def test_tokenize_and_stem():
    #tokenize, stem, and remove stop words
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_0.parse()
    test_string_input_0 = ""
    test_list_output_0 = []
    assert indexer_0.tokenize_and_stem(test_string_input_0) == test_list_output_0

    test_string_input_1 = "crayola"
    test_list_output_1 = ["crayola"]
    assert indexer_0.tokenize_and_stem(test_string_input_1) == test_list_output_1

    test_string_input_2 = "make a phone call tonight and begin calling cousins and siblings"
    test_list_output_2 = ["make", "phone", "call", "tonight", "begin", "call", "cousin", "sibl"]
    assert indexer_0.tokenize_and_stem(test_string_input_2) == test_list_output_2

    test_string_input_3 = "cars automobiles trains running and kayaking or swims"
    test_list_output_3 = ["car", "automobil", "train", "run", "kayak", "swim"]
    assert indexer_0.tokenize_and_stem(test_string_input_3) == test_list_output_3

def test_remove_stop_stem():
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_0.parse()
    # checking for stop word remover functionality
    assert indexer_0.tokenize_and_stem("") == [] # not functional base case?
    assert indexer_0.tokenize_and_stem("and") == []
    assert indexer_0.tokenize_and_stem("or") == []
    assert indexer_0.tokenize_and_stem("if") == [] #is this one

    # checking for stemmer functionality
    assert indexer_0.tokenize_and_stem("hold") == ["hold"]
    assert indexer_0.tokenize_and_stem("artery") == ["arteri"] # "artery"?
    assert indexer_0.tokenize_and_stem("arteries") == ["arteri"]
    assert indexer_0.tokenize_and_stem("keys") == ["key"]
    assert indexer_0.tokenize_and_stem("keying") == ["key"] 
    assert indexer_0.tokenize_and_stem("keyed") == ["key"] 


def test_euclidean_distance():
    indexer_page_rank_example_1 = Indexer("PageRankExample1.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    test_dict_iteration_0 = {
        1 : 0.3333,
        2 : 0.3333,
        3 : 0.3333
    }
    
    test_dict_iteration_1 = {
        1 : 0.4750,
        2 : 0.1916,
        3 : 0.3333
    }

    test_dict_iteration_2 = {
        1 : 0.4148,
        2 : 0.2519,
        3 : 0.3333
    }

    test_dict_iteration_3 = {
        1 : 0.4404,
        2 : 0.2263,
        3 : 0.3333
    }

    test_dict_iteration_4 = {
        1 : 0.4295,
        2 : 0.2272,
        3 : 0.3333
    }

    test_dict_iteration_5 = {
        1 : 0.4341,
        2 : 0.2325,
        3 : 0.3333
    }

    test_dict_iteration_6 = {
        1 : 0.4322,
        2 : 0.2345,
        3 : 0.3333
    }

    test_dict_iteration_7 = {
        1 : 0.4330,
        2 : 0.2337,
        3 : 0.3333
    }

    test_dict_iteration_8 = {
        1 : 0.4326,
        2 : 0.2340,
        3 : 0.3333
    }

    #using hand calculated numbers -- numbers from handout are incorrect
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_0, test_dict_iteration_1) - 0.2003)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_1, test_dict_iteration_2) - 0.0852)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_2, test_dict_iteration_3) - 0.0362)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_3, test_dict_iteration_4) - 0.0109)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_4, test_dict_iteration_5) - 0.0070)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_5, test_dict_iteration_6) - 0.0028)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_6, test_dict_iteration_7) - 0.0012)  <= 0.0001
    assert abs(indexer_page_rank_example_1.euclidean_distance(test_dict_iteration_7, test_dict_iteration_8) - 0.0005)  <= 0.0001

    

def test_weight():
    indexer_page_rank_example_1 = Indexer("PageRankExample1.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_page_rank_example_1.parse()

    # page links: dict of (id of doc) -> (set of ids linked to by doc)

    # list of pages in PageRankExample1:
    # id 1: A
    # id 2: B
    # id 3: C
    assert pytest.approx(indexer_page_rank_example_1.weight(1, 2)) == 0.475
    assert pytest.approx(indexer_page_rank_example_1.weight(1, 3)) == 0.475
    assert pytest.approx(indexer_page_rank_example_1.weight(2, 1)) == 0.475
    assert pytest.approx(indexer_page_rank_example_1.weight(2, 3)) == 0.475

    assert pytest.approx(indexer_page_rank_example_1.weight(3, 1)) == 0.9

    assert pytest.approx(indexer_page_rank_example_1.weight(1, 1)) == 0.05
    assert pytest.approx(indexer_page_rank_example_1.weight(2, 2)) == 0.05
    assert pytest.approx(indexer_page_rank_example_1.weight(3, 3)) == 0.05
    assert pytest.approx(indexer_page_rank_example_1.weight(3, 2)) == 0.05


#ALREADY DONE IN PARSE
def test_calculate_t_f(): # is tf testing already covered by one of the dictionaries written to in the parse testing
    pass

def test_calculate_idf(): # same as tf?
    pass

# -------------------------------------------------------------------------

def test_indexer_parse():
    
    # simple_wiki_0 test cases
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_0.parse()
    assert indexer_0.ids_to_titles.get(1) == "Soda"
    assert indexer_0.titles_to_ids.get("Soda") == 1

    # for the word soda in document with id 0, does it appear 1 times
    assert indexer_0.words_ids_counts.get("soda").get(1) == 1

    # tf for soda in document 0 = 1
    # idf = log(1/1) = 0
    assert indexer_0.words_ids_relevance.get("soda").get(1) == 0

    
    # assert indexer_0.parse(
    #     "/Users/satchwaldman/Desktop/cs0200/projects/ \
    #     search-PVIP35-satchwaldman/simple_wiki_0.xml") == "soda"

    # -----------------------------------------------------------------------
    
    indexer_1 = Indexer("simple_wiki_1.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    # assert indexer_1.parse(
    #     "/Users/satchwaldman/Desktop/cs0200/projects/ \
    #     search-PVIP35-satchwaldman/simple_wiki_1.xml") \
    #         == "Cars are sometimes known as automobiles \
    #             This is a delicious sauce used for dipping"

    # -----------------------------------------------------------------------

    indexer_2 = Indexer("simple_wiki_2.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_2.parse()

    # id numbers
    assert indexer_2.titles_to_ids.get("Car") == 1
    assert indexer_2.titles_to_ids.get("Truck") == 2
    assert indexer_2.titles_to_ids.get("Scooter") == 3
    assert indexer_2.titles_to_ids.get("Banana") == 4


    # c_i_j
    assert indexer_2.words_ids_counts.get("automobil").get(1) == 1
    assert indexer_2.words_ids_counts.get("automobil").get(2) == 1

    assert indexer_2.words_ids_counts.get("meant").get(1) == 1

    assert indexer_2.words_ids_counts.get("go").get(1) == 1
    assert indexer_2.words_ids_counts.get("go").get(2) == 1

    assert indexer_2.words_ids_counts.get("road").get(1) == 2
    assert indexer_2.words_ids_counts.get("road").get(2) == 1

    assert indexer_2.words_ids_counts.get("poorli").get(1) == 1

    assert indexer_2.words_ids_counts.get("suit").get(1) == 1

    # assert indexer_2.words_ids_counts.get("off").get(1) == 1 #is this a stop word?
    # assert indexer_2.words_ids_counts.get("off").get(2) == 1

    assert indexer_2.words_ids_counts.get("travel").get(1) == 1

    assert indexer_2.words_ids_counts.get("unlik").get(1) == 1

    assert indexer_2.words_ids_counts.get("truck").get(1) == 1

    assert indexer_2.words_ids_counts.get("similar").get(2) == 1
    assert indexer_2.words_ids_counts.get("similar").get(3) == 1

    assert indexer_2.words_ids_counts.get("car").get(2) == 1
    assert indexer_2.words_ids_counts.get("car").get(3) == 1

    assert indexer_2.words_ids_counts.get("four").get(2) == 2

    assert indexer_2.words_ids_counts.get("wheel").get(2) == 2
    assert indexer_2.words_ids_counts.get("wheel").get(3) == 1

    assert indexer_2.words_ids_counts.get("drive").get(2) == 1

    assert indexer_2.words_ids_counts.get("two").get(3) == 1

    assert indexer_2.words_ids_counts.get("delici").get(4) == 1

    assert indexer_2.words_ids_counts.get("fruit").get(4) == 1

    assert indexer_2.words_ids_counts.get("carri").get(4) == 1

    # relevance
    assert abs(indexer_2.words_ids_relevance.get("automobil").get(1) - 0.35)  <= 0.01
    assert abs(indexer_2.words_ids_relevance.get("automobil").get(2) - 0.35)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("meant").get(1) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("go").get(1) - 0.35)  <= 0.01
    assert abs(indexer_2.words_ids_relevance.get("go").get(2) - 0.35)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("road").get(1) - 0.69)  <= 0.01
    assert abs(indexer_2.words_ids_relevance.get("road").get(2) - 0.35)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("poorli").get(1) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("suit").get(1) - 0.69)  <= 0.01

    # assert indexer_2.words_ids_relevance.get("off").get(1) == pytest.approx(0.35)
    # assert indexer_2.words_ids_relevance.get("off").get(2) == pytest.approx(0.35)

    assert abs(indexer_2.words_ids_relevance.get("travel").get(1) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("unlik").get(1) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("truck").get(1) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("similar").get(2) - 0.35)  <= 0.01
    assert abs(indexer_2.words_ids_relevance.get("similar").get(3) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("car").get(2) - 0.35)  <= 0.01
    assert abs(indexer_2.words_ids_relevance.get("car").get(3) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("four").get(2) - 1.39)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("wheel").get(2) - 0.69)  <= 0.01
    assert abs(indexer_2.words_ids_relevance.get("wheel").get(3) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("drive").get(2) - 0.69)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("two").get(3) - 1.39)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("delici").get(4) - 1.39)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("fruit").get(4) - 1.39)  <= 0.01

    assert abs(indexer_2.words_ids_relevance.get("carri").get(4) - 1.39)  <= 0.01

   # -----------------------------------------------------------------------

    indexer_link_1 = Indexer("link_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")
    indexer_link_1.parse()

    # id numbers
    assert indexer_link_1.titles_to_ids.get("Dogs") == 1
    assert indexer_link_1.titles_to_ids.get("Cats") == 2
    assert indexer_link_1.titles_to_ids.get("Bird") == 3
    assert indexer_link_1.titles_to_ids.get("Monkey") == 4

    # c_i_j
    assert indexer_link_1.words_ids_counts.get("bird").get(1) == 1
    assert indexer_link_1.words_ids_counts.get("bird").get(2) == 1
    assert indexer_link_1.words_ids_counts.get("bird").get(3) == 1
    assert indexer_link_1.words_ids_counts.get("bird").get(4) == 2

    assert indexer_link_1.words_ids_counts.get("walk").get(1) == 1

    assert indexer_link_1.words_ids_counts.get("monkey").get(1) == 1
    assert indexer_link_1.words_ids_counts.get("monkey").get(2) == 3

    assert indexer_link_1.words_ids_counts.get("cat").get(1) == 1
    assert indexer_link_1.words_ids_counts.get("cat").get(4) == 1

    assert indexer_link_1.words_ids_counts.get("fenc").get(1) == 1
    assert indexer_link_1.words_ids_counts.get("fenc").get(3) == 1

    assert indexer_link_1.words_ids_counts.get("allig").get(2) == 1

    assert indexer_link_1.words_ids_counts.get("tree").get(2) == 1
    assert indexer_link_1.words_ids_counts.get("tree").get(3) == 1

    assert indexer_link_1.words_ids_counts.get("flight").get(3) == 1

    assert indexer_link_1.words_ids_counts.get("dog").get(3) == 2
    assert indexer_link_1.words_ids_counts.get("dog").get(4) == 2

    assert indexer_link_1.words_ids_counts.get("fenc").get(1) == 1
    assert indexer_link_1.words_ids_counts.get("fenc").get(3) == 1

    assert indexer_link_1.words_ids_counts.get("banana").get(4) == 1

    assert indexer_link_1.words_ids_counts.get("count").get(4) == 1

    # relevance
    assert indexer_link_1.words_ids_relevance.get("bird").get(1) == 0
    assert indexer_link_1.words_ids_relevance.get("bird").get(2) == 0
    assert indexer_link_1.words_ids_relevance.get("bird").get(3) == 0
    assert indexer_link_1.words_ids_relevance.get("bird").get(4) == 0

    assert abs(indexer_link_1.words_ids_relevance.get("walk").get(1) - 1.39) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("monkey").get(1) - 0.69) <= 0.01
    assert abs(indexer_link_1.words_ids_relevance.get("monkey").get(2) - 0.69) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("cat").get(1) - 0.69) <= 0.01
    assert abs(indexer_link_1.words_ids_relevance.get("cat").get(4) - 0.35) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("fenc").get(1) - 0.69) <= 0.01
    assert abs(indexer_link_1.words_ids_relevance.get("fenc").get(3) - 0.35) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("allig").get(2) - 0.46) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("tree").get(2) - 0.23) <= 0.01
    assert abs(indexer_link_1.words_ids_relevance.get("tree").get(3) - 0.35) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("flight").get(3) - 0.69) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("dog").get(3) - 0.69) <= 0.01
    assert abs(indexer_link_1.words_ids_relevance.get("dog").get(4) - 0.69) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("banana").get(4) - 0.69) <= 0.01

    assert abs(indexer_link_1.words_ids_relevance.get("count").get(4) - 0.69) <= 0.01

    # -----------------------------------------------------------------------
                                #Page Rank
    # -----------------------------------------------------------------------

    # *** Does Page Rank make sense without a query? Can we just standalone
    #     test it like this?

    # NOTE: everything here indexes at 1

def test_indexer_page_rank():
    # Expected: Rank(A) = 0.4326, Rank(B) = 0.2340, Rank(C) = 0.3333
    indexer_page_rank_1 = Indexer("PageRankExample1.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_page_rank_1.parse()
    # is it correct to treat node A as id 1, etc (according to xml)
    assert abs(indexer_page_rank_1.ids_ranks.get(1) - 0.4326)  <= 0.0001
    assert abs(indexer_page_rank_1.ids_ranks.get(2) - 0.2340) <= 0.0001 # should we do this? (checking if value is within some error)
    assert abs(indexer_page_rank_1.ids_ranks.get(3) - 0.3333) <= 0.0001

    assert indexer_page_rank_1.page_most_common_apppearances.get(1) == 1
    # second doc has no text (should we test this?)
    assert indexer_page_rank_1.page_most_common_apppearances.get(3) == 1

    # assert indexer_page_rank_1.page_links.get(0) == 2
    # assert indexer_page_rank_1.page_links.get(1) == 0 # is this correct to do?
    # assert indexer_page_rank_1.page_links.get(2) == 1

    assert 2 in indexer_page_rank_1.page_links.get(1)
    assert 3 in indexer_page_rank_1.page_links.get(1)

    #nothing in .get(2)

    assert 1 in indexer_page_rank_1.page_links.get(3)

    # -----------------------------------------------------------------------

    # Expected: Rank(A) = 0.2018, Rank(B) = 0.0375, Rank(C) = 0.3740, Rank(D) = 0.3867
    indexer_page_rank_2 = Indexer("PageRankExample2.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_page_rank_2.parse()

    assert abs(indexer_page_rank_2.ids_ranks.get(1) - 0.2018)  <= 0.0001
    assert abs(indexer_page_rank_2.ids_ranks.get(2) - 0.0375)  <= 0.0001
    assert abs(indexer_page_rank_2.ids_ranks.get(3) - 0.3740)  <= 0.0001
    assert abs(indexer_page_rank_2.ids_ranks.get(4) - 0.3867)  <= 0.0001

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
    indexer_page_rank_3 = Indexer("PageRankExample3.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_page_rank_3.parse()

    assert abs(indexer_page_rank_3.ids_ranks.get(1) - 0.0524)  <= 0.0001
    assert abs(indexer_page_rank_3.ids_ranks.get(2) - 0.0524)  <= 0.0001
    assert abs(indexer_page_rank_3.ids_ranks.get(3) - 0.4476)  <= 0.0001
    assert abs(indexer_page_rank_3.ids_ranks.get(4) - 0.4476)  <= 0.0001

    assert indexer_page_rank_3.page_most_common_apppearances.get(1) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(2) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(3) == 1
    assert indexer_page_rank_3.page_most_common_apppearances.get(4) == 1

    assert 2 in indexer_page_rank_3.page_links.get(1)
    assert 3 in indexer_page_rank_3.page_links.get(1)
    assert 4 in indexer_page_rank_3.page_links.get(1)

    assert 1 in indexer_page_rank_3.page_links.get(2)
    assert 3 in indexer_page_rank_3.page_links.get(2)
    assert 4 in indexer_page_rank_3.page_links.get(2)

    assert 4 in indexer_page_rank_3.page_links.get(3)

    assert 3 in indexer_page_rank_3.page_links.get(4)

    # -----------------------------------------------------------------------

    # Expected: Rank(A) = 0.0375, Rank(B) = 0.0375, Rank(C) = 0.4625, Rank(D) = 0.4625
    indexer_page_rank_4 = Indexer("PageRankExample4.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_page_rank_4.parse()

    assert abs(indexer_page_rank_4.ids_ranks.get(1) - 0.0375)  <= 0.0001
    assert abs(indexer_page_rank_4.ids_ranks.get(2) - 0.0375)  <= 0.0001
    assert abs(indexer_page_rank_4.ids_ranks.get(3) - 0.4625)  <= 0.0001
    assert abs(indexer_page_rank_4.ids_ranks.get(4) - 0.4625)  <= 0.0001

    assert indexer_page_rank_4.page_most_common_apppearances.get(1) == 3
    assert indexer_page_rank_4.page_most_common_apppearances.get(2) == 1
    assert indexer_page_rank_4.page_most_common_apppearances.get(3) == 1
    assert indexer_page_rank_4.page_most_common_apppearances.get(4) == 2

    assert 3 in indexer_page_rank_4.page_links.get(1)
    assert 4 in indexer_page_rank_4.page_links.get(2)
    assert 4 in indexer_page_rank_4.page_links.get(3)
    assert 3 in indexer_page_rank_4.page_links.get(4)

    # -----------------------------------------------------------------------

    
    indexer_0 = Indexer("simple_wiki_0.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_0.parse()
    # computing PageRank with no edges (connections between pages)?
    #assert indexer_0.ids_ranks.get(1) == 1 # is this correct for base case?
    assert indexer_0.page_most_common_apppearances.get(1) == 1 # only one word
    #doesn't make sense to test on the page_links dictionary because the values (set of links for each doc) is an empty set

    
    indexer_1 = Indexer("simple_wiki_1.xml",
        "titles.txt",
        "docs.txt",
        "words.txt")

    indexer_1.parse()
    # MANUAL PAGE RANK CALCS:
    # none of the pages in this wiki link to one another
    # still a useful base case
    assert abs(indexer_1.ids_ranks.get(0) - 0.5) <= 0.1 # both should be equal and sum to 1 because they (the docs) are not related?
    assert abs(indexer_1.ids_ranks.get(1) - 0.5) <= 0.1

    # a_j = max(i) (c_i_j) (how many term i in doc j)
    assert indexer_1.page_most_common_apppearances.get(0) == 1 # each word appears once