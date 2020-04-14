import nltk
from newspaper import Article
from geograpy4.places import PlaceContext
from geograpy4.geocoder import geocoder

class Extractor(object):
    def __init__(self,value = None,ignoreEstablishments=True):
        #I anticipate the establishments feature will be pretty unreliable for a long time coming, add option to ignore that feature and only focus on the cities.
        self.ignoreEstablishments = ignoreEstablishments
        if not value:
            raise Exception('url or text is required')
        self.value = value
        self.places = []
        self.validLabels = ["GPE","ORGANIZATION","FACILITY","PERSON"]
        self.geocoder = geocoder()
        self.set_text() #Grab the text if not directly provided

    def set_text(self):
        try: 
            a = Article(self.value)
            a.download()
            a.parse()
            self.text = a.text
        except: self.text = self.value
        del self.value

    def convertGPELabels(self,values):
        pc = PlaceContext(values)
        pc.set_countries()
        pc.set_cities()
        return {"CITY":pc.cities,"COUNTRY":pc.countries}

    def buildQueries(self,tag):
        query = []
        for key in tag: 
            if len(tag[key])==0: tag[key].append("") #Make sure key value pairs don't return empty

        if self.ignoreEstablishments:
            for City        in tag["CITY"]:
                for Country in tag["COUNTRY"]:
                    queryValue = "{} {}".format(City,Country)
                    if queryValue not in query: query.append(queryValue)
        else:
            for Organization        in tag["ORGANIZATION"]:
                for Facility        in tag["FACILITY"]:
                    for City        in tag["CITY"]:
                        for Country in tag["COUNTRY"]:
                            queryValue = "{} {} {} {}".format(Organization,Facility,City,Country)
                            if queryValue not in query: query.append(queryValue)
        return query

    def filterByContext(self):
        returnListCities = []
        returnListCountries = []
        #If the sentence has mentioned a city or country already, only use that
        for value in self.tag["GPE"]:
            if value in self.tag["CITY"]:
                returnListCities.append(value)
            if value in self.tag["COUNTRY"]:
                returnListCountries.append(value)

        #If returnListCities and returnListCountries have no values, that means that it wasn't mentioned in the sentence. Due to this ambigiuity, use all possible values
        if len(returnListCities) > 0 : self.tag["CITY"]=returnListCities
        if len(returnListCountries)>0: self.tag["COUNTRY"]=returnListCountries

    def get_query_from_sentences(self,sentence):
        #In a given sentence, a location will either come by itself or come paired with other information
        #Example, "In New York there is a fancy restruant called Krispy Kreme" -> "Krispy Kremes, New York"
        #Example, "Two musuems in Washington DC is the Simithsonian National Museum and the National Gallery of Art" -> "Simithsonian National Museum, Washington DC" and "National Gallery of Art, Washington DC"
        #Example, "I really like Cancun, Mexico" -> "Cancun, Mexico"
        #TODO: I will currently write the code to ignore the possibility that a location includes a name (ie. "St.George's Square"), this functionality should be added in the future
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
        self.tag = dict(list(tag.items()) + list(self.convertGPELabels(tag["GPE"]).items()))

        #Filter the possible combinations by context
        self.filterByContext()

        query = self.buildQueries(self.tag)
        return query

    def find_entities(self,addressOnly=False):
        self.sentences = nltk.sent_tokenize(self.text) #Grab the sentences
        self.queries = []

        #Build a query list
        for sentence in self.sentences:
            self.queries = self.queries + self.get_query_from_sentences(sentence)

        #Clean the output
        returnList = [item for item in self.geocoder.queryList(self.queries,addressOnly=addressOnly) if item != None]

        #Query said list to build a database
        return returnList