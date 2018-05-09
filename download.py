# No copyright ChristopherABurns@gmail.com 5/7/18
# Pseudo Code:
# iterate through the energy types
# iterate through the collection of pages - for each energy type
# iterate through the image table of each page - for each energy type
# save each image as 'name-of-the-pokemon.png'
# the file name will later be the label of the image
# yes, I use camel notation. #OldPeopleCode

import os
import time
import urllib
import urllib2
from bs4 import BeautifulSoup

hitCounter = 0  # The hit counter tels us when to pause the download so that Pokemon.com doesn't give us a 503 error

baseUrl = "https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/"

energyTypes = ['?card-grass=on', '?card-lightning=on', '?card-darkness=on', '?card-fairy=on', '?card-fire=on',
               '?card-psychic=on', '?card-metal=on', '?card-dragon=on', '?card-water=on', '?card-fighting=on',
               '?card-colorless=on']


# replace any invalid filename characters prior to writing an image to disk
def namecleaner(origFileName):
    filename = str(origFileName)
    if filename.find('?') > -1:
        print("? Character found in filename - replacing...")
        filename = filename.replace('?', '_')

    if filename.find('*') > -1:
        print("* Character found in filename - replacing...")
        filename = filename.replace('*', '_')

    return filename


# make three attempts to read a URL response with Beautiful Soup
def makesoup(currentUrl):
    global hitCounter
    if hitCounter == 9:
        print("resetting connection... sleeping for 60 seconds")
        time.sleep(60)
        print("re-establishing connection...")
        # Connect to a different site to reset the connection to Pokemon
        response = urllib2.urlopen('https://www.google.com')
        response.close()
        hitCounter = 0
    print("Calling URL: {}".format(currentUrl))

    for attempt in range(1, 3):
        try:
            response = urllib2.urlopen(currentUrl)
            soup = BeautifulSoup(response.read(), 'html.parser')
            time.sleep(1)
            response.close()
            hitCounter = hitCounter + 1
            print ('{} successful connections made...'.format(str(hitCounter)))
            return soup
        except Exception as e:
            if attempt == 0:
                print('First connection attempt failed, trying again in 1 second')
                time.sleep(1)
            elif attempt == 1:
                print('Second connection attempt failed, trying again in 2 seconds')
                time.sleep(2)
            elif attempt == 2:
                print('Third connection attempt failed. Unable to connect to Pokemon site: {}'.format(e.message))
                time.sleep(3)


def getAllByEnergyType(energyType = '', spec_range=[1, 99]):
    if energyType == '':
        exit()
    else:
        # make first connection to get pagination information
        currentUrl = baseUrl + energyType
        soup = makesoup(currentUrl)

        # find the HTML DIV tag with the number of pages
        divCounter = soup.find("div", {"id": "cards-load-more"})

        # extract the span tag from the DIV
        spans = divCounter.findAll("span")
        if len(spans) == 3:
            spanContents = ''.join(spans[1].contents)

        # extract the total number of pages for this energy type
        numOfPageParts = spanContents.split(' ', 2)
        numOfPages = int(numOfPageParts[2])

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
                    # convert to string for easier splitting
                    strImage = str(image)
                    # get the pokemon's name from the link's alt attribute
                    pokemonName = strImage[strImage.index('alt="') + 5: strImage.index('src') - 2]
                    # get the URL of the image file
                    imgUrl = strImage[strImage.index('src="') + 5: strImage.index('"/>')]
                    # spit the URL to get the original filename
                    parts = strImage.split('_', 2)
                    origfileName = parts[2][0:parts[2].index('"')]
                    # clean the pokemon name
                    cleanpokemonName = namecleaner(pokemonName)
                    # create a new file name from the clean pokemon name and the original image file name
                    newFileName = cleanpokemonName + '_' + origfileName
                    # check for the a pre-existing copy of this file and write to disk
                    if os.path.isfile('./images/' + dirName + '/' + newFileName) is not True:
                        urllib.urlretrieve(imgUrl, './images/' + dirName + '/' + newFileName)
                        print("downloaded {}".format(newFileName))
                    time.sleep(1)
            except ValueError as e:
                print("ERROR! {}".format(e.message))


for etype in energyTypes:

    parts = etype.split('-')
    dirName = parts[1][0: parts[1].index('=')]
    if os.path.isdir('./images/' + dirName) is not True:
        os.makedirs('./images/' + dirName)  # Create the directory of needed
    print('Downloading {} Pokemon card images'.format(dirName))

    # This was a hack to pick up where an interrupted download stopped.
    # If your download fails or is interrupted - enter the Energy type you were on when the error occurred, and the page
    # that you were on when the error occurred - rerun the script and it will pick up where it left off.
    # !!! don't forget to intent the call to getAllByEnergyType(type)
    '''
    if type == '?card-water=on':
        spec_range = [70,99]
        getAllByEnergyType('?card-water=on', spec_range)
    else:
    '''
    getAllByEnergyType(etype)

