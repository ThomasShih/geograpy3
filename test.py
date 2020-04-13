import geograpy4

a = geograpy4.get_place_context("I really like Union Station in Toronto from Canada",addressOnly=True)
for result in a:
    print(result)

#geograpy4.get_place_context(text="Hi my name is Thomas and I am drinking at Bob's Tavern in Califorina")