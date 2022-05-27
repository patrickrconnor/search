import sys
import file_io
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import re

STOP_WORDS = set(stopwords.words("english"))  # store a set of stopwords


class Indexer:
    """This is a class that contains code to index an xml file, i.e process an
    XML document into a list of terms, determine the relevance between terms and
    documents, and determine the authority of each document."""

    def __init__(
        self,
        xml_filepath: str,
        titles_filepath: str,
        docs_filepath: str,
        words_filepath: str,
    ):
        """Initialization method for the Indexer class."""
        self.xml_filepath = xml_filepath
        self.titles_filepath = titles_filepath
        self.docs_filepath = docs_filepath
        self.words_filepath = words_filepath

        # Intiatiate all the necessary data structures as empty
        self.ids_to_titles: dict[int:str] = {}
        self.titles_to_ids: dict[str:int] = {}
        self.words_ids_counts: dict[str : dict[int:int]] = {}
        self.words_ids_relevance: dict[str : dict[int:float]] = {}
        self.ids_ranks: dict[int:float] = {}
        self.page_most_common_apppearances: dict[int:int] = {}
        self.page_links: dict[int : set[int]] = {}

    def extract_title(self, page):
        """Extracts the title from a page

        Parameters:
        page- an xml page

        Returns:
        A string corresponding to the title of the page"""
        return page.find("title").text.strip()

    def extract_id(self, page):
        """Extracts the id from a page

        Parameters:
        page- an xml page

        Returns:
        An integer corresponding to the id of the page"""
        return int(page.find("id").text.strip())

    def extract_text(self, page):
        """Extracts the text from a page

        Parameters:
        page- an xml page

        Returns:
        A string corresponding to the text of the page"""
        return page.find("text").text.strip()

    def parse(self):
        """Parses the input xml file, appropriately constructing the neccesary
        data structures

        Side effects:
        Populates ids_to_titles and titles_to_id dictionaries
        Stores a list of page ids
        Populates the words_ids_counts dictionary
        Populates words_ids_relevance dictionary
        Makes a call to page_rank to appropriate calculate and store pagerank
        information
        """
        root = et.parse(self.xml_filepath).getroot()
        all_pages = root.findall("page")
        # Store the total amount of pages
        self.n = len(all_pages)
        # Populate ids_to_titles and titles_to_ids dictionaries
        for page in all_pages:
            self.id = self.extract_id(page)
            title = self.extract_title(page)
            self.ids_to_titles[self.id] = title
            self.titles_to_ids[title] = self.id
        # Store list of page ids
        self.page_ids = list(self.titles_to_ids.values())
        for page in all_pages:
            self.id = self.extract_id(page)
            self.page_links[self.id] = []
            # Store a list of tokenized and stem words as page corpus
            page_corpus = self.tokenize_and_stem(self.extract_text(page))
            # Intatiate most common appearing number for the page to be zero
            self.page_most_common_apppearances[self.id] = 0
            # Loop through each word in the corpus and store how many times a
            # word appears on each page
            for word in page_corpus:
                if word in self.words_ids_counts:
                    if self.id in self.words_ids_counts[word]:
                        self.words_ids_counts[word][self.id] += 1
                    else:
                        self.words_ids_counts[word][self.id] = 1
                else:
                    self.words_ids_counts[word] = {}
                    self.words_ids_counts[word][self.id] = 1
                # Store the number of appearances of the most common word
                self.page_most_common_apppearances[self.id] = max(
                    self.page_most_common_apppearances[self.id],
                    self.words_ids_counts[word][self.id],
                )
        # Calculate the relevance of a word on a page, using the formulas for idf
        # and tf.
        for word in self.words_ids_counts:
            n_i = len(self.words_ids_counts[word])
            self.words_ids_relevance[word] = {}
            for id in self.words_ids_counts[word]:
                c_i_j = self.words_ids_counts[word][id]
                a_i_j = self.page_most_common_apppearances[id]
                self.words_ids_relevance[word][id] = (
                    c_i_j / a_i_j * math.log(self.n / n_i)
                )
        # Call page_rank to appropriately store page_rank information
        self.page_rank(self.page_ids)

    def tokenize_and_stem(self, words: str):
        """Takes the text of a page and appropriately outputs a list of the
        tokenized and stemmed text, also handles links.

        Parameters:
        words- a string corresponding to the text of a page

        Returns:
        A list of words, containing the appropriate text in the input string,
        tokenized, stemmed and with the stop words removed.

        Side effects:
        Populates the page_link dictionary with each page_id the given page
        links to"""
        stemmer = PorterStemmer()
        link_regex = r"\[\[[^\[]+?\]\]"
        word_regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
        all_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
        all_text = re.findall(all_regex, words)
        word_text = []
        for match in all_text:
            # Check if the word is a link
            if re.match(link_regex, match):
                split_link = match.strip("[,]").split("|")
                link_title = split_link[0]
                # Check if link is in corpus
                if link_title in self.titles_to_ids:
                    # Store id of link
                    link_id = self.titles_to_ids[link_title]
                    # Check if it's not a self link
                    if self.id != link_id:
                        # Check if link id isn't already counted
                        if link_id not in self.page_links[self.id]:
                            # Count the link_id
                            self.page_links[self.id].append(link_id)
                if len(split_link) > 1:
                    link_text = split_link[1]
                else:
                    link_text = link_title
                # Add the text of the link to the word_text list
                word_text += re.findall(word_regex, link_text)
            else:
                word_text.append(match)
        # Check if page has no links
        if len(self.page_links[self.id]) == 0:
            # If page has no links, add all the page ids to it's page_links
            # dictionary
            self.page_links[self.id] = self.page_ids.copy()
            # Remove it's own id from it's page_links dictionary
            self.page_links[self.id].remove(self.id)
        return [stemmer.stem(x) for x in word_text if x not in STOP_WORDS]

    def euclidean_distance(self, r: dict[int:float], r_prime: dict[int:float]):
        """Calculates Euclidean distance between two iterations of pagerank,
        r and r prime

        Parameters:
        r - a dictionary of ids to ranks corresponding to one iteration of
        page_rank
        r-prime a dictionary of ids to ranks corresponding to the next iteration
        of page_rank

        Returns:
        A float corresponding to the euclidean distance between r and r-prime"""
        sum_counter = 0
        r_values = list(r.values())
        r_prime_values = list(r_prime.values())
        for i in range(len(r_values)):
            # Sums the squared difference of each value of r-prime - each value
            # of r
            sum_counter += (r_prime_values[i] - r_values[i]) ** 2
        return math.sqrt(sum_counter)

    def weight(self, k: int, j: int):
        """Determines the weight a page k, gives to a page j.

        Parameters:
        k - an int representing a page id
        j- an int representing a second page id

        Returns:
        A float representing weight that k gives to a j"""
        # Check again if k has no links
        if self.page_links[k] == []:
            # If the page has no links, add all the page ids to it's page_links
            # dictionary
            self.page_links[k] = self.page_ids.copy()
            # Remove it's own id from it's page_links dictionary
            self.page_links[k].remove(k)
        # Check if k links to j:
        if j in self.page_links[k]:
            # Apply link weight formula
            return 0.15 / self.n + 0.85 / len(self.page_links[k])
        else:
            # Apply non-linking formula
            return 0.15 / self.n

    def page_rank(self, page_ids):
        """Determines the authority of each document, populates the id to
        pagerank dictionary.

        Side Effects:
        Calls euclidean_distance and weight to properly populate id to pagerank
        dictionary"""
        # Intatiate an empty dictionary to hold an iteration of page rank
        r: dict[int:float] = {}
        # Intatiate each entry of r to be 0.0
        for id in page_ids:
            r[id] = 0.0
            # Store each current page rank to be 1/n
            self.ids_ranks[id] = 1 / self.n
        while self.euclidean_distance(r, self.ids_ranks) > 0.001:
            # r is a set of 1/n
            r = self.ids_ranks.copy()
            for j in page_ids:
                # Apply pagrank formula
                self.ids_ranks[j] = 0
                for k in page_ids:
                    self.ids_ranks[j] = (
                        self.ids_ranks[j] + self.weight(k, j) * r[k]
                    )


# This is the main method that runs the program
if __name__ == "__main__":
    # Check if input is appropriate length
    if len(sys.argv) - 1 == 4:
        # create an instance of the Indexer class with the given input
        indexer = Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        # Parse the input
        indexer.parse()
        # Appropriately write the dictionaries to the appropriate files
        file_io.write_title_file(indexer.titles_filepath, indexer.ids_to_titles)
        file_io.write_docs_file(indexer.docs_filepath, indexer.ids_ranks)
        file_io.write_words_file(
            indexer.words_filepath, indexer.words_ids_relevance
        )
    else:
        print(
            "The input should be of the form <XML filepath> <titles filepath> <docs filepath> <words filepath>"
        )
