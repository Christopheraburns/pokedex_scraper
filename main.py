'''
Pseudo Code:
iterate through the energy types
iterate through the collection of pages (for each energy type)
iterate through the image table
save each image as 'name-of-the-pokemon.png"

'''
import os
import time
import urllib
import urllib2
from bs4 import BeautifulSoup

global dirName

baseUrl = "https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/"

#grass type was used for debugging - don't forget to add it back to the below collection
energyTypes = ['?card-lightning=on', '?card-darkness=on', '?card-fairy=on', '?card-fire=on',
               '?card-psychic=on', '?card-metal=on', '?card-dragon=on', '?card-water=on', '?card-fighting=on', '?card-colorless=on']
totPagesNum = 0



def makesoup(currentUrl):
    print("Calling URL: {}".format(currentUrl))
    for attempt in range(1,3):
        try:
            response = urllib2.urlopen(currentUrl)
            soup = BeautifulSoup(response.read(), 'html.parser')
            time.sleep(1)
            response.close()
            return soup
        except Exception as e:
            if attempt == 0:
                print('First connection attempt failed, trying again in 1 second')
                time.sleep(1)
            elif attempt == 1:
                print('Second connectoion attempt failed, trying again in 2 seconds')
                time.sleep(2)
            elif attempt == 2:
                print('Third connection attempt failed, trying again in 3 seconds')
                time.sleep(3)
            else:
                print("Error! {}{}".format("Unable to connect to Pokemon site:", e.message))




def getAllByEnergyType(energyType = '', spec_range=[]):
    if energyType == '':
        exit()
    else:
        currentUrl = baseUrl + energyType
        soup = makesoup(currentUrl)

        # find the HTML DIV tag with the number of pages
        divCounter = soup.find("div", {"id": "cards-load-more"})

        # extract the span tag from the DIV
        spans = divCounter.findAll("span")
        if(len(spans) == 3):
            spanContents = ''.join(spans[1].contents)

        # extract the number of pages
        numOfPageParts = spanContents.split(' ', 2)

        numOfPages = int(numOfPageParts[2])

        pageCounter = 1
        for pages in range(spec_range[0], numOfPages + 1):
            if pages == 0:
                pass # Web pages are not zero based
            elif pages == 1:
                # first page is not enumerated
                currentUrl = baseUrl + energyType
            else:
                currentUrl = baseUrl + str(pages) + energyType
            try:
                soup = makesoup(currentUrl)
                # find the unordered list of cards for this page
                unordered_list = soup.find('ul', class_='cards-grid clear')

                # isolate just the img tags
                images = unordered_list.findAll("img")

                # extract the link to the image and the name of the pokemon
                for image in images:
                    # convert to String for easier splitting
                    strImage = str(image)
                    pokemonName = strImage[strImage.index('alt="') + 5: strImage.index('src') - 2]
                    imgUrl = strImage[strImage.index('src="') + 5: strImage.index('"/>')]
                    parts = strImage.split('_', 2)
                    origfileName = parts[2][0:parts[2].index('"')]
                    newFileName = pokemonName + '_' + origfileName

                    if os.path.isfile('./images/' + dirName + '/' + newFileName) is not True:
                        urllib.urlretrieve(imgUrl, './images/' + dirName + '/' + newFileName)
                        print("downloaded {}".format(newFileName))
                    time.sleep(1)
            except ValueError as e:
                print("ERROR! {}".format(e.message))

for type in energyTypes:
    #if type == '?card-grass=on':
        #spec_range = [76,99]
        #getAllByEnergyType('?card-grass=on', spec_range)
    parts = type.split('-')
    dirName = parts[1][0: parts[1].index('=')]

    os.makedirs('./images/' + dirName)
    getAllByEnergyType(type)

