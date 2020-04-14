s = """I was in Thailand until last week, decided to leave because I was in Phuket and the situation seemed to be getting worse by the day. :( Plus the airport was scheduled to be closed through my visa expiration date and they hadn’t announced the free extension policy yet.

I was contemplating going to NYC, that’s where my parents are, though I haven’t lived in the US for 6 years. But then the US blew up in cases so that was no longer a viable option.

My last resort was to return to Japan, where I have dual citizenship. I just got back last week. It sucks because I just uprooted my life of 6 years here this past January to travel long term and I feel like I’ve taken a huge step backwards. I don’t have an address, health insurance, etc here anymore so for now I’m staying with a friend indefinitely and helping him pay the bills because he’s out of work due to covid.

Reading the stories of stranded tourists in Thailand, I realize I got off pretty lucky in this situation but I’m really hoping that things improve soon so I can leave Japan again. I would prefer to go explore the rest of Southeast Asia but I won’t make any decisions until I have an idea of what season it’ll be when I can travel again (don’t want to be somewhere during monsoon season for example). Until then, laying low at my friend’s place, trying to stay productive with some freelance work, and trying to keep my expenses as low as possible so I don’t have to dip into my travel funds while waiting for the storm to pass.
"""
import geograpy4

print(geograpy4.get_place_context(s,addressOnly=True))