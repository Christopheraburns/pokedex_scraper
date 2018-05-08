'''
Pseudo Code:
iterate through the energy types
iterate through the collection of pages (for each energy type)
iterate through the image table
save each image as 'name-of-the-pokemon.png"

'''

import urllib
from bs4 import BeautifulSoup


baseUrl = "https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/?"
curPageNum = 1  #page 1 is not numbered!
energyTypes = ['card-grass=on', 'card-lightning=on', 'card-darkness=on', 'card-fairy=on', 'card-fire=on',
               'card-psychic=on', 'card-metal', 'card-dragon=on', 'card-water=on', 'card-fighting=on', 'card-colorless=on']
totPagesNum = 0
currentUrl = ""

for type in energyTypes:
    curPageNum = '' #reset this to 1 - which means no numeric value
    currentUrl = baseUrl + curPageNum



def getAllByEnergyType(energyType = ''):
    if energyType == '':
        exit()
    else:
        # build the url - assume we are starting at page 1
        currentUrl = baseUrl + energyType




