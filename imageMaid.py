# No copyright ChristopherABurns@gmail.com 6/12/18
# Pseudo Code:
# iterate through the images in a given directory to: (simple to add a recursive function to do multiple dirs)
# identify the average file size (on disk) of the images
# remove files that are less than 10% of the file size of the average file size - those are too small to work with
# rename or convert all image files to .jpg for consistency
# hash each image and use the hash to check for duplicates - remove any duplicates discovered
# create a list of the different image sizes (height and width) - note the minimum and recommend uniform dimension
# resize images to the chosen uniform dimension

import time
import os
import cv2
import numpy as np
from glob import glob
from PIL import Image
import imagehash
from pydblite.pydblite import Base
import sys

basepath = "./dataset/"
subdirlist = []

# supply a list of classes (objects) to create a dataset
listitems = open('cars.txt', 'r')
for item in listitems:
    subdirlist.append(item)


def resize(classdir, height, width):
    global basepath
    filecount = len(glob(classdir + "/*.jpg"))
    index = 0

    # by default save images to a new directory
    newdir = os.path.basename(os.path.normpath(classdir))
    newdir = newdir + "_" + str(height) + "x" + str(width)
    newpath = basepath + newdir
    if not os.path.isdir(newpath):
        os.makedirs(basepath + newdir)

    for imagePath in glob(classdir + "/*.jpg"):
        index = index + 1
        try:
            img = cv2.imread(imagePath)
            # method #1 - minimalistic crop to achieve proper aspect ratio THEN scale down.
            # (images currently smaller than the height + width parameters will not be scaled.

            # method #2 - no cropping - simply scale the image width to the width parameter and keep the aspect ratio
            # add padding to a dimension if necessary
            r = 800.0/img.shape[1]
            h = int(img.shape[0] * r)
            dim = (width, h)
            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            # do we pad? If height is less than 600 we will pad.
            if h < 600:
                # split the difference and add padding to top and bottom
                diff = 600 - h
                if not diff%2 == 0:
                    # the difference is not divisible by 2
                    # round the half difference to the nearest whole and subtract it from the difference to get the padding
                    toppad = diff/2
                    toppad = int(round(toppad))
                    botpad = diff - toppad
                else:
                    toppad = diff/2
                    botpad = toppad
                resized = cv2.copyMakeBorder(resized, toppad, botpad, 0, 0, cv2.BORDER_REPLICATE)

            cv2.imwrite(newpath + '/' + os.path.basename(imagePath), resized)
            sys.stdout.write("resizing image #{} of {} \r".format(index, filecount))
            sys.stdout.flush()
            time.sleep(0.1)
        except Exception, e:
            print('error resizing/padding image: {} . message: {}'.format(imagePath, e.message))
            continue


def inventoryshape(classdir):
    filecount = len(glob(classdir + "/*.jpg"))
    print('determining optimal image resolution...')
    db = Base('shape', save_to_file=False)
    db.create('filename', 'height', 'width', 'count')
    index = 0
    for imagePath in glob(classdir + "/*.jpg"):
        index = index + 1
        try:
            img = cv2.imread(imagePath)
            filename = os.path.basename(imagePath)
            shape = img.shape
            h = shape[0]
            w = shape[1]
            pre = db(height=h, width=w)
            # see if there is already an image of this shape in the DB...
            if pre:
                # ...if so - update the count
                rec_id = pre[0]['__id__']
                counter = int(pre[0]['count'])
                counter = counter + 1
                record = db[rec_id]
                db.update(record, count=counter)
            else:
                # ...if not - insert the new shape
                db.insert(filename=filename, height=h, width=w, count=1)
            sys.stdout.write("reading shape for image #{} of {} \r".format(index, filecount ))
            sys.stdout.flush()
            time.sleep(0.1)
        except Exception, e:
            print('error processing image {}: {}'.format(imagePath, e))
            continue

    # need to add some more intelligence to this bit of code to auto-select the best image size
    heightchk = db("height") < 590
    heightcounter = 0
    for r in heightchk:
        heightcounter = heightcounter + 1
    print('{} images ({}%) may lose fidelity by converting to 600x800 pixels'.format(heightcounter,
                                                                                     heightcounter / filecount))


def getstats(classdir):

    try:
        filelist = os.listdir(classdir.strip())
        print("class count: {} ".format(len(filelist)))

        # get the average file size for this class
        filesizelist = []
        for file in filelist:
            filesizelist.append(os.path.getsize(classdir.strip() + "/" + file))

        # Convert to Numpy - because Numpy is better
        npfilesize = np.asarray(filesizelist)
        # print("class avg filesize: {} kb".format(np.average(npfilesize) / 1024))
        # print("class mean filesize): {} kb".format(np.mean(npfilesize / 1024)))
        # print("class minimum filesize: {} bytes".format(np.min(npfilesize)))
        # print("class maximum filesize: {} kb".format(np.max(npfilesize / 1024)))
        # print("______________________________________")
        # print("                                      ")

        cutoff = np.average(npfilesize / 10)

        for file in filelist:
            path = classdir.strip() + "/" + file
            size = os.path.getsize(path)
            if size < cutoff:
                print("deleting file {} it is only {} bytes ({} kb)".format(file, size, size / 1024))
                os.remove(path)

        # recalculate AVG size
        # get the average file size for this class
        filelist = os.listdir(classdir.strip())
        filesizelist = []
        for file in filelist:
            filesizelist.append(os.path.getsize(classdir.strip() + "/" + file))

        # Convert to Numpy - because Numpy is better
        npfilesize = np.asarray(filesizelist)
        # print("new class avg filesize (post-processing): {} kb".format(np.average(npfilesize) / 1024))
        # print("new class mean filesize (post-processing): {} kb".format(np.mean(npfilesize / 1024)))
        # print("new class minimum filesize (post-processing): {} kb".format(np.min(npfilesize / 1024)))
        # print("new class maximum filesize (post-processing): {} kb".format(np.max(npfilesize / 1024)))
        # print("                                     ")
        # print("*************************************")
        # print("                                     ")
    except Exception, e:
        print('Error in the getstats() function: {}'.format(e.message))


def convertrename(classdir):
    pngs = glob(classdir + '/*.png')
    if len(pngs) > 0:
        for p in pngs:
            # print('Converting {} to .jpg file'.format(p))
            try:
                img = cv2.imread(p)
                cv2.imwrite(p[:-3] + 'jpg', img)
            except Exception, e:
                print('Error converting {} to JPG format'.format(p))
                continue
    else:
        print('No .PNG files detected')

    jpegs = glob(classdir + '/*.jpeg')
    if len(jpegs) > 0:
        for j in jpegs:
            try:
                basename = os.path.splitext(j)[0]
                newname = basename + '.jpg'
                # print('renaming {} to {}.jpg file'.format(j, basename))
                os.rename(j, newname)
            except Exception, e:
                print('Error renaming {} to .JPG format'.format(j))
                continue
    else:
        print('No .JPEG files detected')


def detectduplicates(classdir):

        # Create an in-memory database
        db = Base('fingerprinter', save_to_file=False)
        db.create('filename', 'hash')
        filecount = len(glob(classdir + "/*.jpg"))
        duplicatecount = 0
        print("creating image fingerprints for de-duplication ...")
        index = 0
        for imagePath in glob(classdir + "/*.jpg"):
            index = index + 1
            try:
                if os.path.exists(imagePath):
                    image = Image.open(imagePath)
                    h = str(imagehash.dhash(image))
                    filename = os.path.basename(imagePath)
                    sys.stdout.write("fingerprint created for image # {} of {} \r".format(index, filecount))
                    sys.stdout.flush()
                    time.sleep(0.1)
                    pre = db(hash=h)
                    if pre:
                        # This image is a duplicate - delete it
                        duplicatecount = duplicatecount + 1
                        os.remove(classdir + "/" + filename)
                    else:
                        db.insert(filename=filename, hash=h)
            except Exception, e:
                print('Error in detectduplicates() function: {}'.format(e))
                continue

        print('Hashing complete.  {} duplicate images were removed from this class repository'.format(duplicatecount))


def processclass(classdir):
    try:
        if os.path.isdir(classdir):
            getstats(classdir)
            print("removing images that are less than 10% of the average filesize ...")
            print("this will remove any 0kb files and hopefully any corrupt files prior to analyzing with OpenCV...")
            print("                                      ")
            print("also converting all .png and renaming .jpeg images to .jpg for consistency")
            convertrename(classdir)

            # detect and delete duplicates
            detectduplicates(classdir)

            # take an inventory of the image sizes
            inventoryshape(classdir)

            # re-format image size with opencv
            resize(classdir, 600, 800)
        else:
            print('Unable to find directory: {} Skipping that class.'.format(classdir))
    except Exception, e:
        print(str(e))


for subdir in subdirlist:
    classdir = os.path.join(basepath, subdir.strip())
    print("\n\n\n")
    print("*********************")
    print("class:: {} ".format(subdir.strip()))

    processclass(classdir.strip())










