import geograpy4

a = geograpy4.get_place_context("The I like both the Union Station in New York and Washington in the United States",addressOnly=True,ignoreEstablishments=False)
for result in a:
    print(result)

#geograpy4.get_place_context(text="Hi my name is Thomas and I am drinking at Bob's Tavern in Califorina")