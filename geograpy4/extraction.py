import nltk
from newspaper import Article
from geograpy4.places import PlaceContext
from geograpy4.geocoder import geocoder

class Extractor(object):
    def __init__(self, url = None, text = None):
        if not url and not text:
            raise Exception('url or text is required')
        self.url = url
        self.text = text
        self.places = []
        self.validLabels = ["GPE","ORGANIZATION","FACILITY","PERSON"]
        self.geocoder = geocoder()
    def set_text(self):
        if not self.text and self.url:
            a = Article(self.url)
            a.download()
            a.parse()
            self.text = a.text

    def convertGPELabels(self,values):
        pc = PlaceContext(values)
        #TODO: Place Context needs to be overhauled
        pc.set_countries()
        pc.set_regions()
        pc.set_cities()
        pc.set_other()
        return {"CITY":pc.cities,"COUNTRY":pc.countries}

    def get_query_from_sentences(self,sentence):
        #In a given sentence, a location will either come by itself or come paired with other information
        #Example, "In New York there is a fancy restruant called Krispy Kreme" -> "Krispy Kremes, New York"
        #Example, "Two musuems in Washington DC is the Simithsonian National Museum and the National Gallery of Art" -> "Simithsonian National Museum, Washington DC" and "National Gallery of Art, Washington DC"
        #Example, "I really like Cancun, Mexico" -> "Cancun, Mexico"
        #TODO: I will currently write the code to ignore the possibility that a location includes a name (ie. "St.George's Square"), this functionality should be added in the future
        #TODO: Code also needs to be written to enliminate results of "Toronto, Australia" if Canada was mentioned in the sentence
        text = nltk.word_tokenize(sentence)
        nes = nltk.ne_chunk(nltk.pos_tag(text))

        #Create a dictionary of place values acquired by NLTK
        tag = dict((label,[]) for label in self.validLabels)
        for ne in nes:
            if type(ne) is nltk.tree.Tree:
                if (ne.label() in self.validLabels):
                    value = u' '.join([i[0] for i in ne.leaves()])
                    tag[ne.label()].append(value)

        #Convert Geopolitical entries to their type (City, Region, Country)
        tag = dict(list(tag.items()) + list(self.convertGPELabels(tag["GPE"]).items()))

        #TODO: Earlier code should have broken up the sentences into single GPE, Facility/Organization pairs already because of this the proceeding code will just look at tall the possible combinations to build queries
        query = []
        for key in tag: tag[key].append("") #Make sure key value pairs don't return empty

        for Organization        in tag["ORGANIZATION"]:
            for Facility        in tag["FACILITY"]:
                for City        in tag["CITY"]:
                    for Country in tag["COUNTRY"]:
                        queryValue = "{} {} {} {}".format(Organization,Facility,City,Country)
                        if queryValue not in query: query.append(queryValue)

        return query

    def find_entities(self):
        self.set_text() #Grab the text if not directly provided
        self.sentences = nltk.sent_tokenize(self.text) #Grab the sentences
        queries = []

        #Build a query list
        for sentence in self.sentences:
            self.queries = queries + self.get_query_from_sentences(sentence)

        #Query said list to build a database
        return self.geocoder.queryList(self.queries)

        # for ne in nes:
        #     if type(ne) is nltk.tree.Tree:
        #         if (ne.label() == 'GPE' or ne.label() == 'PERSON' or ne.label() == 'ORGANIZATION'):
        #             value = u' '.join([i[0] for i in ne.leaves()])
        #             self.places.append(value)