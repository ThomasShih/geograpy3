import os
import inspect
import csv
import sqlite3
from collections import Counter

import jellyfish
import pycountry


# hat tip http://stackoverflow.com/a/1342373/2367526
def remove_non_ascii(s):
    """Function used to remove non-ascii characters."""
    return "".join(i for i in s if ord(i) < 128)


def fuzzy_match(s1, s2, max_dist=.8):
    """Function that checks if two strings match."""
    return jellyfish.jaro_distance(s1, s2) >= max_dist

"""
Takes a list of place names and works place designation (country, region, etc.)
and relationships between places (city is inside region is inside country, etc.)
"""


class PlaceContext(object):
    """Class that matches strings to places."""

    def __init__(self, place_names, db_file = None):
        """Init method."""
        db_file = db_file or \
            os.path.dirname(os.path.realpath(inspect.stack()[0][1])) + "/locs.db"
        self.conn = sqlite3.connect(db_file)
        if not self.db_has_data():
            self.populate_db()

        self.places = place_names

    def populate_db(self):
        """Method used to populate the data db."""
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS cities")

        table_creation = '''CREATE TABLE cities
            (geoname_id INTEGER,
             continent_code TEXT,
             continent_name TEXT,
             country_iso_code TEXT,
             country_name TEXT,
             subdivision_iso_code TEXT,
             subdivision_name TEXT,
             city_name TEXT,
             metro_code TEXT,
             time_zone TEXT)'''
        cur.execute(table_creation)
        cur_dir = os.path.dirname(os.path.realpath(inspect.stack()[0][1]))
        with open(cur_dir + "/data/GeoLite2-City-Locations.csv", "r", encoding = 'utf8') as info:
            reader = csv.reader(info)
            for row in reader:
                cur.execute("INSERT INTO cities VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)

            self.conn.commit()

    def db_has_data(self):
        """Method used to check if the db has the data correctly."""
        cur = self.conn.cursor()

        cur.execute("SELECT Count(*) FROM sqlite_master WHERE name='cities';")
        data = cur.fetchone()[0]

        if data > 0:
            cur.execute("SELECT Count(*) FROM cities")
            data = cur.fetchone()[0]
            return data > 0

        return False

    def correct_country_mispelling(self, s):
        """Method used to correct country mispellings."""
        cur_dir = os.path.dirname(os.path.realpath(inspect.stack()[0][1]))
        with open(cur_dir + "/data/ISO3166ErrorDictionary.csv", "r", encoding = 'utf8') as info:
            reader = csv.reader(info)
            for row in reader:
                if s in remove_non_ascii(row[0]):
                    return row[2]

        return s

    def is_country(self, s): 
        try: return True if pycountry.countries.get(name=s) else False
        except: return False

    def is_region(self,place_name, region_names):
        return filter(lambda rn: self.region_match(place_name, rn),region_names)

    def region_match(self,place_name, region_name):
        return fuzzy_match(remove_non_ascii(place_name),
                            remove_non_ascii(region_name))

    def places_by_name(self, place_name, column_name):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM cities WHERE ' + column_name + ' = "' + place_name + '"')
        rows = cur.fetchall()

        if len(rows) > 0:
            return rows

        return None

    def cities_for_name(self, city_name):
        return self.places_by_name(city_name, 'city_name')

    def regions_for_name(self, region_name):
        return self.places_by_name(region_name, 'subdivision_name')

    def get_region_names(self, country_name):
        country_name = self.correct_country_mispelling(country_name)
        try:
            obj = pycountry.countries.get(name=country_name)
            regions = pycountry.subdivisions.get(country_code=obj.alpha2)
        except:
            regions = []

        return [r.name for r in regions]

    def set_countries(self):
        """Method used to find all matching countries."""
        places = [self.correct_country_mispelling(place) for place in self.places]
        countries = [place for place in places if self.is_country(place)]
        self.country_mentions = Counter(countries).most_common()
        self.countries = list(set(countries))

    def set_regions(self):
        """Method used to find all matching regions."""
        regions = []
        self.country_regions = {}
        region_names = {}

        if not self.countries:
            self.set_countries()

        for country in self.countries:
            region_names = self.get_region_names(country)
            matched_regions = [p for p in self.places if self.is_region(p, region_names)]
            regions += matched_regions
            self.country_regions[country] = list(set(matched_regions))

        self.region_mentions = Counter(regions).most_common()
        self.regions = list(set(regions))

    def set_cities(self):
        """Method used to find all matching cities."""
        self.cities = []
        self.country_cities = {}
        self.address_strings = []

        if not self.regions:
            self.set_regions()

        cur = self.conn.cursor()
        table_query = "SELECT * FROM cities WHERE city_name IN (" + \
                      ",".join("?" * len(self.places)) + ")"
        cur.execute(table_query, self.places)
        rows = cur.fetchall()

        for row in rows:
            country = None

            try:
                country = pycountry.countries.get(alpha2=row[3])
                country_name = country.name
            except KeyError:
                country_name = row[4]

            city_name = row[7]
            region_name = row[6]

            if city_name not in self.cities:
                self.cities.append(city_name)

            if country_name not in self.countries:
                self.countries.append(country_name)
                self.country_mentions.append((country_name, 1))

            if country_name not in self.country_cities:
                self.country_cities[country_name] = []

            if city_name not in self.country_cities[country_name]:
                self.country_cities[country_name].append(city_name)

                if country_name in self.country_regions and \
                   region_name in self.country_regions[country_name]:
                    self.address_strings.append(city_name + ", " +
                                                region_name + ", " +
                                                country_name)

        all_cities = [p for p in self.places if p in self.cities]
        self.city_mentions = Counter(all_cities).most_common()

    def set_other(self):
        """Method used when the found data is not found."""
        if not self.cities:
            self.set_cities()

        def unused(place_name):
            places = [self.countries, self.cities, self.regions]
            return all(self.correct_country_mispelling(place_name)
                       not in l for l in places)

        self.other = [p for p in self.places if unused(p)]
        
