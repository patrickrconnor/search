import xml.etree.ElementTree as et
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import re

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
        self.words_ids_counts: dict[str : dict[int:int]] = {}
        self.words_ids_relevance: dict[str : dict[int:float]] = {}
        self.ids_ranks: dict[int:float] = {}
        self.page_most_common_apppearances: dict[int:int] = {}

    def extract_title(self, page):
        return page.find("title").text

    def extract_id(self, page):
        return int(page.find("id").text)

    def extract_text(self, page):
        return page.find("text").text

    def parse(self, xml_filepath: str):
        root = et.parse(xml_filepath).getroot()
        all_pages = root.findall("page")
        n = len(all_pages)
        for page in all_pages:
            id = self.extract_id(page)
            self.ids_to_titles[id] = self.extract_title(page)
            page_corpus = self.tokenize_and_stem(self.extract_text(page))
            self.page_most_common_apppearances[id] = 0
            for word in page_corpus:
                if word in self.words_ids_counts:
                    if id in self.words_ids_counts[word]:
                        self.words_ids_counts[word][id] += 1
                    else:
                        self.words_ids_counts[word][id] = 1
                else:
                    self.words_ids_counts[word] = {}
                    self.words_ids_counts[word][id] = 1
                self.page_most_common_apppearances[id] = max(
                    self.page_most_common_apppearances[id],
                    self.words_ids_counts[word][id],
                )
        for word in self.words_ids_counts:
            n_i = len(self.words_ids_counts[word])
            for id in self.words_ids_counts[word]:
                self.words_ids_relevance[word] = {}
                c_i_j = self.words_ids_counts[word][id]
                a_i_j = self.page_most_common_apppearances[id]
                self.words_ids_counts[word][id] = c_i_j / a_i_j * math.log(n / n_i)

    def tokenize_and_stem(self, words: str):
        link_regex = """\[\[[^\[]+?\]\]"""
        all_words_regex = """[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"""
        return [self.remove_stop_stem(x) for x in re.findall(all_words_regex, words)]

    def remove_stop_stem(self, word: str):
        stemmer = PorterStemmer()
        if word not in STOP_WORDS:
            return stemmer.stem(word)
