# No copyright ChristopherABurns@gmail.com 6/12/18
# Pseudo Code:
# iterate through the images in a given directory to: (simple to add a recursive function to do multiple dirs)
# identify the average file size (on disk) of the images
# remove files that are less than 10% of the file size of the average file size - those are too small to work with
# rename or convert all image files to .jpg for consistency
# hash each image and use the hash to check for duplicates - remove any duplicates discovered
# create a list of the different image sizes (height and width) - note the minimum and recommend uniform dimension
# resize images to the chosen uniform dimension

from requests import exceptions
import requests
import cv2
import os

API_KEY = "1ed0dcd4006f47378a74376709139879"
#API_KEY = "YOUR_API_KEY_HERE"
MAX_RESULTS = 2500  # keep this "lower" to keep the relevance and the quality of the results higher
GROUP_SIZE = 50

URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

EXCEPTIONS = set([IOError,
                  exceptions.RequestException, exceptions.HTTPError,
                  exceptions.ConnectionError, exceptions.Timeout])


def searchanddownload(classtype, output):
    term = classtype

    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": term, "offset": 0, "count": GROUP_SIZE}

    # make the search
    print("[INFO] searching API for '{}'".format(term))
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()

    # grab the results frm the search
    results = search.json()
    estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
    print("[INFO] {} total results for '{}'".format(estNumResults, term))

    # total downloads so far
    total = 0

    # loop over the estimated number of results
    for offset in range(0, estNumResults, GROUP_SIZE):
        # update the search param using the current offset
        print("[INFO] making request for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
        params["offset"] = offset
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()
        print("[INFO] saving images for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))

        # loop over the results
        for v in results["value"]:
            # try to download the image
            try:
                # make a request to download the image
                print("[INFO] fetching: {}".format(v["contentUrl"]))
                r = requests.get(v["contentUrl"], timeout=30)

                # build the path to the output image
                ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                p = os.path.sep.join([output, "{}{}".format(str(total).zfill(8), ext)])

                # write the image to disk
                f = open(p, "wb")
                f.write(r.content)
                f.close()

            # catch any errors
            except Exception as e:
                if type(e) in EXCEPTIONS:
                    print("[INFO] skipping: {} because: {}".format(v["contentUrl"], e.message))
                    continue

            image = cv2.imread(p)

            if image is None:
                print("[INFO] deleting: {}".format(p))
                os.remove(p.strip())
                continue
            total += 1

# Load the master list of classes
classlist = []
classes = open('cars.txt', 'r')
for classtype in classes:
    classlist.append(classtype)

# initiate search for each class
for classtype in classlist:
    output = 'dataset/' + str(classtype).strip()
    # create the directory
    if os.path.exists('./dataset/' + str(classtype).strip()) is not True:
        os.makedirs('./dataset/' + str(classtype).strip())
    searchanddownload(classtype, output)


