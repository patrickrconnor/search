import xml.etree.ElementTree as et

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
        self.words_ids_relevance: dict[str : dict[int:float]] = {}
        self.ids_ranks: dict[int:float] = {}

    def extract_title(self, page):
        return page.find("title").text

    def extract_id(self, page):
        return int(page.find("id").text)

    def parse(self, xml_filepath: str):
        root: Element = et.parse(xml_filepath).getroot()
        all_pages: ElementTree = root.findall("page")
        for page in all_pages:
            pass
