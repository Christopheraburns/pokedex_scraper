# no copyright - 5/9/2018 ChristopherABurns@gmail.com
# remove special characters, spaces, EC and GX designation from imagefile.
import os
import shutil

deletedfiles = []
global masterlist
basepath = './images/raw_form/245x342_TCG_images_mixed/'
processedpath = './images/processed/245x342_TCG_images_mixed/'


#  the word alolan from the name
def removealolan(filename):
    #print 'checking {} for variations of alolan'.format(filename)
    if filename.find('alolan ') > -1:
        filename = filename.replace('alolan ', '')

    if filename.find('ALOLAN ') > -1:
        filename = filename.replace('ALOLAN ', '')

    if filename.find('Alolan ') > -1:
        filename = filename.replace('Alolan ', '')

    return filename


# break versoin of cards will only confuse the training since they are usually horizontally oriented and all gold
def checkforbreak(filename):
    result = False
    if filename.find('BREAK') > -1:
        result = True
        os.remove(basepath + filename)
        deletedfiles.append('{} was deleted as it was a break version of the pokemon and not suited for training'
                                .format(filename))
    if filename.find('LEGEND') > -1:
        result = True
        os.remove(basepath + filename)
        deletedfiles.append('{} was deleted as it was a LEGEND version of the pokemon and not suited for training'
                        .format(filename))

    return result

# remove and GX of EX initials
def removeGXEX(filename):
    if filename.find('GX') > -1:
        filename = filename.replace('GX', '')
    if filename.find('EX') > -1:
        filename = filename.replace('EX', '')
    if filename.find('[G]') > -1:
        filename = filename.replace('[G]', '')
    if filename.find(' ex') > -1:
        filename = filename.replace(' ex', '')
    if filename.find('FB') > -1:
        filename = filename.replace('FB', '')
    if filename.find('Ash') > -1:
        filename = filename.replace('Ash', '')
    if filename.find("Ash's ") > -1:
        filename = filename.replace("Ash's ", '')
    if filename.find("Dark ") > -1:
        filename = filename.replace("Dark ", '')
    if filename.find("Black ") > -1:
        filename = filename.replace("Black ", '')
    if filename.find("Team Aqua's ") > -1:
        filename = filename.replace("Team Aqua's ", '')
    if filename.find("Ultra ") > -1:
        filename = filename.replace('Ultra ', '')

    return filename


def clean(filename):
    newarray = []

    # remove GX or EX
    filename = removeGXEX(filename)

    # remove alolan
    filename = removealolan(filename)

    # split at the underscore and ignore anything AFTER the underscore
    if filename.find('_') > -1:
        parts = filename.split('_')
        underscore = parts[0]
    else:
        underscore = filename

    #split at the first SPACE and ignore anyting AFTER the space
    if underscore.find(' ') > -1:
        parts = underscore.split(' ')
        chararray = list(parts[0])
    else:
        chararray = list(underscore)

    # check for special characters first
    for letter in chararray:
        #print 'letter {} = ASCII {}'.format(letter, ord(letter))
        if 65 <= ord(letter) <= 90:  # A-Z - acceptable
            newarray.append(letter)
        else:
            if 97 <= ord(letter) <= 122:  # a-z - acceptable
                newarray.append(letter)

    newname = ''.join(newarray)

    return newname

toprocess = os.listdir(basepath)
masterlist = []
# testlimit = 1000
# counter = 1
for f2p in toprocess:

    # if counter == testlimit:
        # break
    if checkforbreak(f2p) == False:
        cleanname = clean(f2p)

        # add this name to the master list
        masterlist.append(cleanname)
        # count the number of instances this name is in the list
        occ = masterlist.count(cleanname)
        # rename the file appropriately
        cleanname = cleanname + '_' + str(occ) + '_p.png'
        print '{} becomes {}'.format(f2p, cleanname)
        shutil.copy(basepath + f2p, processedpath)
        os.rename(processedpath + f2p, processedpath + cleanname)
    # counter = counter + 1
