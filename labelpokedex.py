from bs4 import BeautifulSoup
import os

soup = BeautifulSoup(open("pokedex_sourceview.html"), "html.parser")

masterlist = soup.find("ul", {"id": "master_list"})
links = masterlist.findAll("a")

for link in links:
    strLink = str(link)
    content = strLink[strLink.index('">') + 2: strLink.index('</')]
    parts = content.split("-")
    index = (parts[0].strip())
    name = (parts[1].strip())

    # pad the index with zeros to match the files
    if len(index) < 4:
        # add zeros to get to 4 digits
        numZeros = 4 - len(index)
        for zero in range(0, numZeros):
            index = '0' + index

    origFile = os.path.join(os.getcwd(), 'images/POKEMON/' + index + '.png')
    newFileName = os.path.join(os.getcwd(), 'images/POKEMON/' + name + '.png')
    print ('renaming {} to {}'.format(origFile, newFileName))
    if os.path.isfile(origFile):
        os.rename(origFile, newFileName)

