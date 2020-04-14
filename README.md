<b>

TODO: One TODO is left in this version of Geograpy, which is being able to handle names as establishment (ie St'George's Square). This message will be removed when this feature is added.

</b>

Geograpy4
========

Geograpy4 improves upon the work of Geograpy3,2, and 1 by allowing for the search of facility names within a city, country, or region. For example, an input of "I like union station in Washington and New York" will return both the addresses Union Station in DC and NY, instead of just the name of the city, country, and region.

Geograpy4 also improves upon how these are grabbed, the previous version's code now help in the building of queries to search in Nominatim via GeoPy. This will now allow for users to get complete location data in line with GeoPy's geocoder raw return values, which contains much more data than what was currently returned by Geograpy3.

Functionalities are different from Geograpy3,2, and 1. For those who are familar with the previous versions, there is no more return for a places object where you can get cities, regions, or countries. This is because complete address is now returned in an array, or the complete raw geocoded data of which you can build a DataFrame out of and query everything you need and then more.

## Install

Grab the package using `pip` and `git` (this could take a few minutes)
Try using one of the following:

    1. pip install geograpy4

## Getting Started

Import the module, give a URL or text, and presto.

    import geograpy4
    input = "http://www.bbc.com/news/world-europe-26919928"
    more_places = geograpy4.get_place_context(input)
or

    import geograpy4
    input = "Perfect just Perfect! It's a perfect storm for Nairobi"
    more_places = geograpy4.get_place_context(input)

Other optional parameters for get_place_context are:
    **addressOnly=False (Return array of addresses (True) or raw geocoded data (False))**
    **ignoreEstablishments=True (Returns only the country,city,region data (True) or add possible establishment data as well (False))**

Note that the return values for ignoreEstablishments=False are currently not as good as I hope it to be, and I will be improving upon it in the future

## Advanced Usage

Advanced usages are removed. Requests may be considered to add.

## Opening a Ticket

If you have found a bug or issue in Geograpy4, please submit a ticket to the Issues tab above, and describe in as much detail as possible all circumstances, inputs, and outputs surrounding said bug.  Thank you for your help!


## Developers

When creating a new branch that corresponds to an Issue, please include the Issue number at the end of the branch name.
`Example: find-entities-fix-5 would correspond to Issue number 5 regarding the find_entities() method not working.`

When creating a new pull request, again reference/link the Issue number the pull request is fixing so that Issues can be closed after merging.

For branches/pull requests unrelated to Issues, please use standard naming conventions and accurately describe the scope and goal of your code.  If you have any questions do not hesitate to ask, thank you!


## Credits
Geograpy4 was originally forked from [jmbielec's Geograpy3](https://github.com/jmbielec/geograpy3), which was forked from [lesingerouge's geograpy2](https://github.com/lesingerouge/geograpy), who originally forked from [ushahidi's Geograpy](https://github.com/ushahidi/geograpy), according to GitHub.


Geograpy4 uses the following excellent libraries:

* [NLTK](http://www.nltk.org/) for entity recognition
* [newspaper](https://github.com/codelucas/newspaper) for text extraction from HTML
* [jellyfish](https://github.com/sunlightlabs/jellyfish) for fuzzy text match
* [pycountry](https://pypi.python.org/pypi/pycountry) for country/region lookups
* [GeoPy](https://geopy.readthedocs.io/en/stable/) for geocoder lookups

Geograpy4 uses the following data sources:

* [GeoLite2](http://dev.maxmind.com/geoip/geoip2/geolite2/) for city lookups
* [ISO3166ErrorDictionary](https://github.com/bodacea/countryname/blob/master/countryname/databases/ISO3166ErrorDictionary.csv) for common country mispellings _via [Sara-Jayne Terp](https://github.com/bodacea)_
* [Nominatim](https://nominatim.openstreetmap.org/) for address search (through GeoPy)

Hat tip to [Chris Albon](https://github.com/chrisalbon) for the name.

Released under the MIT license.
