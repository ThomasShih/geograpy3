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

def get_place_context(value=None,addressOnly=False,ignoreEstablishments=False):
    e = Extractor(value,ignoreEstablishments=ignoreEstablishments)
    return e.find_entities(addressOnly)