<b>This repo is currently under development to try and include a way of grabing geography keywords or location names instaed of just countries, regions, and cities. All documentation are currently out of date</b>

Geograpy3
========

Geograpy3 fixes issues caused by using Geograpy with later versions of Python 3 (specifically in the Spyder IDE of Anaconda, but should work with Pyhon 3 in general). Most functionalities have remained the same as in Geograpy (and Geograpy2) while others may have changed slightly to work in Python 3.  Its core functionality is to extract place names from a URL or text, and add context to those names -- for example distinguishing between a country, region or city.  For more information on installation, usage, and syntax, please continue reading below.

## Install

Grab the package using `pip` and `git` (this could take a few minutes)
Try using one of the following:

    1. pip install git+git://github.com/jmbielec/geograpy3.git 
    2. pip install git+https://github.com/jmbielec/geograpy3.git 

## Getting Started

Import the module, give a URL or text, and presto.

    import geograpy3
    link = 'http://www.bbc.com/news/world-europe-26919928'
    places = geograpy3.get_place_context(url = link)
    
    text_input = "Perfect just Perfect! It's a perfect storm for Nairobi"
    more_places = geograpy3.get_place_context(text = text_input)

Now you have access to information about all the places mentioned in the linked 
article. 

* `places.countries` _contains a list of country names_
* `places.regions` _contains a list of region names_
* `places.cities` _contains a list of city names_
* `places.other` _lists everything that wasn't clearly a country, region or city_

Note that the `other` list might be useful for shorter texts, to pull out 
information like street names, points of interest, etc, but at the moment is 
a bit messy when scanning longer texts that contain possessive forms of proper 
nouns (like "Russian" instead of "Russia").

## Advanced Usage

In addition to listing the names of discovered places, you'll also get some 
information about the relationships between places.

* `places.country_regions` _regions broken down by country_
* `places.country_cities` _cities broken down by country_
* `places.address_strings` _city, region, country strings useful for geocoding_

While a text might mention many places, it's probably focused on one or two, so 
Geograpy3 also breaks down countries, regions and cities by number of mentions.

* `places.country_mentions`
* `places.region_mentions`
* `places.city_mentions`

Each of these returns a list of tuples. The first item in the tuple is the place 
name and the second item is the number of mentions. For example:

    [('Russian Federation', 14), (u'Ukraine', 11), (u'Lithuania', 1)]  

## Running Modules Separately

You can of course use each of Geograpy3's modules on their own. For example:

    from geograpy3 import extraction

    e = extraction.Extractor(url = 'http://www.bbc.com/news/world-europe-26919928')
    e.find_entities()

    # You can now access all of the places found by the Extractor
    print(e.places)

Place context is handled in the `places` module. For example:

    from geograpy3 import places

    pc = places.PlaceContext(['Cleveland', 'Ohio', 'United States'])
    
    pc.set_countries()
    print(pc.countries) #['United States']

    pc.set_regions()
    print(pc.regions) #['Ohio']

    pc.set_cities()
    print(pc.cities) #['Cleveland']

    print(pc.address_strings) #['Cleveland, Ohio, United States']

And of course all of the other information shown above (`country_regions` etc) 
is available after the corresponding `set_` method is called.


## Opening a Ticket

If you have found a bug or issue in Geograpy3, please submit a ticket to the Issues tab above, and describe in as much detail as possible all circumstances, inputs, and outputs surrounding said bug.  Thank you for your help!


## Developers

When creating a new branch that corresponds to an Issue, please include the Issue number at the end of the branch name.
`Example: find-entities-fix-5 would correspond to Issue number 5 regarding the find_entities() method not working.`

When creating a new pull request, again reference/link the Issue number the pull request is fixing so that Issues can be closed after merging.

For branches/pull requests unrelated to Issues, please use standard naming conventions and accurately describe the scope and goal of your code.  If you have any questions do not hesitate to ask, thank you!


## Credits
Geograpy3 was originally forked from [lesingerouge's Geograpy](https://github.com/lesingerouge/geograpy), who originally forked from [ushahidi's Geograpy](https://github.com/ushahidi/geograpy), who I believe is the original creator of Geograpy.  Geograpy3 also used some material and inspiration from [Corollarium's Geograpy2](https://github.com/Corollarium/geograpy2).


Geograpy3 uses the following excellent libraries:

* [NLTK](http://www.nltk.org/) for entity recognition
* [newspaper](https://github.com/codelucas/newspaper) for text extraction from HTML
* [jellyfish](https://github.com/sunlightlabs/jellyfish) for fuzzy text match
* [pycountry](https://pypi.python.org/pypi/pycountry) for country/region lookups

Geograpy3 uses the following data sources:

* [GeoLite2](http://dev.maxmind.com/geoip/geoip2/geolite2/) for city lookups
* [ISO3166ErrorDictionary](https://github.com/bodacea/countryname/blob/master/countryname/databases/ISO3166ErrorDictionary.csv) for common country mispellings _via [Sara-Jayne Terp](https://github.com/bodacea)_

Hat tip to [Chris Albon](https://github.com/chrisalbon) for the name.

Released under the MIT license.
