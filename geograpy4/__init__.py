import nltk

from geograpy4.extraction import Extractor
from geograpy4.places import PlaceContext

# download all the basic nltk toolkit
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.downloader.download('averaged_perceptron_tagger')


def get_place_context(url = None, text = None):
    e = Extractor(url = url, text = text)
    e.find_entities()

    pc = PlaceContext(e.places)
    pc.set_countries()
    pc.set_regions()
    pc.set_cities()
    pc.set_other()

    return pc
