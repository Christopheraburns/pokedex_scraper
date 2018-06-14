# No copyright ChristopherABurns@gmail.com 6/12/18
# Code adapted from Adrian Rosebrock (https://realpython.com/fingerprinting-images-for-near-duplicate-detection/)


from PIL import Image
import imagehash
import argparse
import shelve
import glob



