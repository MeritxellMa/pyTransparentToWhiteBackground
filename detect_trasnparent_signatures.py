from PIL import Image
import os
import sys


def get_main_color(image):
    img = Image.open(image)
    colors = img.getcolors(256)  # put a higher value if there are many colors in your image
    max_occurrence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurrence:
                (max_occurrence, most_present) = c
        return most_present[1]
    except TypeError:
        raise Exception("Too many colors in the image")


def is_transparent(color):
    if color != 255:
        # print "is transparent"
        return True
    else:
        # print "is white"
        return False


def through_directories(path, ots):
    for child in os.listdir(path):
        test_path = os.path.join(path, child)
        if os.path.isdir(test_path):
            through_directories(test_path, ots)
        if test_path.endswith('.jpg'):
           try:
               if is_transparent(get_main_color(test_path)):
                    ot=test_path.split('_')
                    ot=ot[0].split('/')
                    ots.add(ot[len(ot)-1])
           except:
               print 'error opening ', test_path

ots = set()
through_directories(sys.argv[1], ots)
sorted_ots = sorted(ots)
for ot in sorted_ots:
    print ot
print 'num damage signatures: ', len(ots)
