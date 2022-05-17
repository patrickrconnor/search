import sys
import file_io
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import re

from pyparsing import empty

STOP_WORDS = set(stopwords.words("english"))

"def index(xml: str, titles_file: str, docs_file: str, words_file: str):"


class Indexer:
    def __init__(
        self,
        xml_filepath: str,
        titles_filepath: str,
        docs_filepath: str,
        words_filepath: str,
    ):
        self.xml_filepath = xml_filepath
        self.titles_filepath = titles_filepath
        self.docs_filepath = docs_filepath
        self.words_filepath = words_filepath

        self.ids_to_titles: dict[int:str] = {}
        self.titles_to_ids: dict[str:int] = {}
        self.words_ids_counts: dict[str : dict[int:int]] = {}
        self.words_ids_relevance: dict[str : dict[int:float]] = {}
        self.ids_ranks: dict[int:float] = {}
        self.page_most_common_apppearances: dict[int:int] = {}
        self.page_links: dict[int : set[int]] = {}

    def extract_title(self, page):
        return page.find("title").text.split("")

    def extract_id(self, page):
        return int(page.find("id").text.split(""))

    def extract_text(self, page):
        return page.find("text").text.split("")

    def parse(self):
        root = et.parse(self.xml_filepath).getroot()
        all_pages = root.findall("page")
        self.n = len(all_pages)
        for page in all_pages:
            self.id = self.extract_id(page)
            title = self.extract_title(page)
            self.ids_to_titles[self.id] = title
            self.titles_to_ids[title] = self.id
        self.page_ids = self.titles_to_ids.values()
        for page in all_pages:
            self.id = self.extract_id(page)
            self.page_links[self.id] = []
            page_corpus = self.tokenize_and_stem(self.extract_text(page))
            self.page_most_common_apppearances[self.id] = 0
            for word in page_corpus:
                if word in self.words_ids_counts:
                    if self.id in self.words_ids_counts[word]:
                        self.words_ids_counts[word][self.id] += 1
                    else:
                        self.words_ids_counts[word][self.id] = 1
                else:
                    self.words_ids_counts[word] = {}
                    self.words_ids_counts[word][self.id] = 1
                self.page_most_common_apppearances[self.id] = max(
                    self.page_most_common_apppearances[self.id],
                    self.words_ids_counts[word][self.id],
                )
        for word in self.words_ids_counts:
            n_i = len(self.words_ids_counts[word])
            for self.id in self.words_ids_counts[word]:
                self.words_ids_relevance[word] = {}
                c_i_j = self.words_ids_counts[word][self.id]
                a_i_j = self.page_most_common_apppearances[self.id]
                self.words_ids_counts[word][self.id] = (
                    c_i_j / a_i_j * math.log(self.n / n_i)
                )
        self.page_rank(self.page_ids)

    def tokenize_and_stem(self, words: str):
        link_regex = r"\[\[[^\[]+?\]\]"
        all_words_regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
        link_text = re.findall(link_regex, words)
        if link_text == []:
            self.page_links[self.id].add(self.page_ids)
            self.page_links[self.id].remove(self.id)
        else:
            for link in link_text:
                page_title = link.strip("[,]").split("|")[0]
                if page_title in self.titles_to_ids:
                    link_id = self.titles_to_ids[page_title]
                    if self.id != link_id:
                        self.page_links[self.id].add(link_id)
        return [
            self.remove_stop_stem(x) for x in re.findall(all_words_regex, words)
        ]

    def remove_stop_stem(self, word: str):
        stemmer = PorterStemmer()
        if word not in STOP_WORDS:
            return stemmer.stem(word)

    def euclidean_distance(self, r: dict[int:float], r_prime: dict[int:float]):
        sum_counter = 0
        r_values = r.values()
        r_prime_values = r_prime.values()
        for i in range(len(r_values)):
            sum_counter += (r_prime_values[i] - r_values[i]) ** 2
        return math.sqrt(sum_counter)

    def weight(self, k: int, j: int):
        if j in self.page_links[k]:
            return 0.15 / self.n + 0.85 / len(self.page__links[k])
        else:
            return 0.15 / self.n

    def page_rank(self, page_ids):
        r: dict[int:float] = {}
        self.n = len(page_ids)
        for page in page_ids:
            id = self.extract_id(page)
            r[id] = 0.0
            self.ids_ranks[id] = 1 / self.n
        while self.euclidean_distance(r, self.ids_ranks) > 0.001:
            r = self.ids_ranks.copy()
            for j in page_ids:
                self.ids_ranks[j] = 0
                for k in page_ids:
                    self.ids_ranks[j] = (
                        self.ids_ranks[j] + self.weight(k, j) * r[k]
                    )


if __name__ == "__main__":
    if len(sys.argv) - 1 == 4:
        indexer = Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        indexer.parse()
        file_io.write_title_file(indexer.titles_filepath, indexer.ids_to_titles)
        file_io.write_docs_file(indexer.docs_filepath, indexer.ids_ranks)
        file_io.write_words_file(
            indexer.words_filepath, indexer.words_ids_relevance
        )
    else:
        print(
            "The input should be of the form <XML filepath> <titles filepath> <docs filepath> <words filepath>"
        )
