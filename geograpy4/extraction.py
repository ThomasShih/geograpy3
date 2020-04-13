import nltk
from newspaper import Article

class Extractor(object):
    def __init__(self, url = None, text = None):
        if not url and not text:
            raise Exception('url or text is required')
        self.url = url
        self.text = text
        self.places = []
        self.validLabels = ["GPE","ORGANIZATION","FACILITY"]

    def set_text(self):
        if not self.text and self.url:
            a = Article(self.url)
            a.download()
            a.parse()
            self.text = a.text


    def find_entities(self):
        self.set_text()

        text = nltk.word_tokenize(self.text)
        nes = nltk.ne_chunk(nltk.pos_tag(text))

        for ne in nes:
            if type(ne) is nltk.tree.Tree:
                if (ne.label() in self.validLabels):
                    value = u' '.join([i[0] for i in ne.leaves()])
                    print(value)
                    self.places.append(value)



        # for ne in nes:
        #     if type(ne) is nltk.tree.Tree:
        #         if (ne.label() == 'GPE' or ne.label() == 'PERSON' or ne.label() == 'ORGANIZATION'):
        #             value = u' '.join([i[0] for i in ne.leaves()])
        #             self.places.append(value)