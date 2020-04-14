import geograpy4

a = geograpy4.get_place_context("St George's Square in London, United Kingdom is a masterpiece.",addressOnly=True,ignoreEstablishments=False)
for result in a:
    print(result)

#geograpy4.get_place_context(text="Hi my name is Thomas and I am drinking at Bob's Tavern in Califorina")