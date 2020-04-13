from geopy.geocoders import Nominatim

class geocoder:
    def __init__(self,user_agent="Geograpy4"):
        self.geoLocater = Nominatim(user_agent=user_agent)
    def queryGeocoder(self,queryString):
        for i in range(3): #Try three times as Nominatim is sometimes unreliable
            try: return self.geoLocater.geocode(queryString,language="en",timeout=3) #I find that the default timeout is too short
            except: return None
        return None #Give up
    def queryList(self,list):
        results = []
        for queryString in list:
            result = self.queryGeocoder(queryString)
            if result: result = result.raw
            if result not in results: results.append(result)
        return results