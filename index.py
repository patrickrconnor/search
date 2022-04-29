import xml.etree.ElementTree as et

"def index(xml: str, titles_file: str, docs_file: str, words_file: str):"

def parse(xml_filepath:str):
    root: Element = et.parse(<xml filepath>).getroot()
    all_pages: ElementTree = root.findall("page")
    for page in all_pages:
        
