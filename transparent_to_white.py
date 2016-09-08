from PIL import Image
from colour import Color


def get_main_color(file):
    img = Image.open(file)
    colors = img.getcolors(256) #put a higher value if there are many colors in your image
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present[1]
    except TypeError:
        raise Exception("Too many colors in the image")

def is_transparent(color):
    if color == 0:
        print "was transparent"
        return True
    else:
        print "is white"
        return False

def transparent_to_white(convert, file, oldDir, newDir):

    img = Image.open(file)

    if convert:
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[3] == 0:
                newData.append((255, 255, 255))
            else:
                newData.append(item)

        img.putdata(newData)

    file = file[len(oldDir):]
    img.save("%s%s" %(newDir, file), "PNG")

for i in range(1, 5):
    oldDir = "original_images/"
    newDir = "generated_images/"
    file = "%sfirma%s.png" % (oldDir, i)
    transparent_to_white(is_transparent(get_main_color(file)), file, oldDir, newDir)
