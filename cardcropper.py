# no copyright 5/9/2018 ChristopherABurns@gmail.com
# pseudo code
# import an image one at a time
# determine the name of the pokemon and add it to a list
# read the list to count the number of instances this pokemon has been processed
# crop the image
# save the new image as <pokemon_#ofInstance_p.png>
# example: there are 3 Abomasnow variations they will be named abomasnow_1_p.png, abomasnow_2_p.png, abomasnow_2_p.png
# the "p" represents "Processed"
# ignore GX images for now - they are "full art" cards and will only confuse the training

import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

masterlist = []
basepath = './images/processed/245x342_TCG_images_mixed/'
savepath = './images/processed/cropped/'

def cropimage(path, filename):
    # verify the file is there
    if os.path.isfile(path + filename):
        print 'cropping {}'.format(filename)
        img = cv2.imread(path + filename)
        cropped = img[41:161, 32:214]
        cv2.imwrite(savepath + filename, cropped)




# get a list of files in the base path directory
toprocess = os.listdir(basepath)
print '{} images to process'.format(len(toprocess))
counter = 0
for f2p in toprocess:
    cropimage(basepath, f2p)
    counter = counter + 1
    print '{} files cropped'.format(str(counter))






