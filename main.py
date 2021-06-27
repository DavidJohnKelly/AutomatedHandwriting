import os
import subprocess
from PIL import Image, ImageFilter
colours = ((255, 255, 255, "white"),
           (200, 100, 50, "orange"),
           (128, 0, 0, "red"),
           (0, 255, 0, "green"),
           (0, 0, 0, "black"),
           (64, 64, 64, "grey")
           )


# Calculates the nearest colour based on the r,g,b values of the pixel and their relation to the saved colours
def nearest_colour(subjects, query):
    return min(subjects, key=lambda subject: sum((s - q) ** 2 for s, q in zip(subject, query)))[3]


originalpicture = Image.open("data/Alphabet.png")
# Enhancing details of original picture for smoother result
width, height = originalpicture.size
picture = originalpicture.resize((width * 2, height * 2), 2)
originalpicture.close()
width, height = picture.size

# Removes the background from the alphabet, leaving only the letters
rgba_image = picture.convert("RGBA")
picture.close()
# Iterating through each pixel in the image
for y in range(height):
    for x in range(width):
        r, g, b, a = rgba_image.getpixel((x, y))
        # Makes any non pen pixels transparent
        if not nearest_colour(colours, (r, g, b)) == "black" and not nearest_colour(colours, (r, g, b)) == "grey":
            rgba_image.putpixel((x, y), (255, 255, 255, 0))
        else:
            rgba_image.putpixel((x, y), (0, 0, 0,))

# Enhancing the letters to be slightly higher quality and more natural looking
detail = rgba_image.filter(ImageFilter.EDGE_ENHANCE)
rgba_image.close()
smooth = detail.filter(ImageFilter.SMOOTH)
sharpen = smooth.filter(ImageFilter.SHARPEN)
smooth.close()
sharpen.save("data/AlphabetAlpha.png")
sharpen.close()

ycroplist = []
'''
Cropping each letter row vertically
Eg A B C D  becomes  A B C D  as two separate files
   E F G H
                     E F G H
'''
rgba_Alphabet = Image.open("data/AlphabetAlpha.png")
# Getting each row where there are no letters
for y in range(height):
    no_letters = True
    for x in range(width):
        r, g, b, a = rgba_Alphabet.getpixel((x, y))
        # Checks if a letter is contained on the current row
        if nearest_colour(colours, (r, g, b)) == "black" or nearest_colour(colours, (r, g, b)) == "grey":
            no_letters = False

    if no_letters:
        ycroplist.append(y)

# Splits the image into the multiple row subimages
verticalcounter = 1
for y in range(len(ycroplist) - 1):
    if not (ycroplist[y] + 1 == ycroplist[y + 1]):
        cropped = rgba_Alphabet.crop((0, ycroplist[y] + 1, width, ycroplist[y + 1]))
        cropped.save("data/VerticalCrop{}.png".format(verticalcounter))
        cropped.close()
        verticalcounter = verticalcounter + 1
rgba_Alphabet.close()

Files = os.listdir("data/")

'''
Cropping each horizontal slice of letters vertically
Eg A B C D becomes A     B     C     D each in their own separate files

'''
horizontalcounter = 1
for item in Files:
    xcroplist = []
    if "VerticalCrop" in item:
        # Splitting each row of letters into their own separate files
        rgba_Alphabet = Image.open("data/" + item)
        width, height = rgba_Alphabet.size
        # Getting each row where there are no letters
        for x in range(width):
            no_letters = True
            for y in range(height):
                r, g, b, a = rgba_Alphabet.getpixel((x, y))
                # Checks if a letter is contained on the current row
                if nearest_colour(colours, (r, g, b)) == "black" or nearest_colour(colours, (r, g, b)) == "grey":
                    no_letters = False

            if no_letters:
                xcroplist.append(x)

        # Splits the image into the multiple row subimages

        for x in range(len(xcroplist) - 1):
            if not (xcroplist[x] + 1 == xcroplist[x + 1]):
                cropped = rgba_Alphabet.crop((xcroplist[x] + 1, 0, xcroplist[x + 1], height))
                cropped.save("data/HorizontalCrop{}.png".format(horizontalcounter))
                cropped.close()
                horizontalcounter = horizontalcounter + 1
        rgba_Alphabet.close()

'''
Crops each letter to completely remove redundant whitespace around the character
'''
Files = os.listdir("data/")
CharacterCounter = 0
for item in Files:
    croplist = []
    if "HorizontalCrop" in item:
        CharacterCounter = CharacterCounter + 1
        rgba_Character = Image.open("data/" + item)
        width, height = rgba_Character.size
        # Finds each row where there is a letter
        for y in range(height):
            for x in range(width):
                r, g, b, a = rgba_Character.getpixel((x, y))
                # Checks if a character is contained on the current row
                if nearest_colour(colours, (r, g, b)) == "black" or nearest_colour(colours, (r, g, b)) == "grey":
                    croplist.append(y)

        # Gets the start and end of the letter and crops the image accordingly
        cropped = rgba_Character.crop((0, croplist[0], width, croplist[len(croplist) - 1]))
        cropped.save(
            "data/characters/Cropped{}.png".format(CharacterCounter))
        # Deletes the redundant files
        os.remove("data/" + item)
        rgba_Character.close()

    elif "VerticalCrop" in item:
        # Deletes the redundant files
        os.remove("data/" + item)
os.remove("data/AlphabetAlpha.png")

'''
Uses SimpleHTR to allocate each cropped image a character
This is a modified version of TensorFlow designed to detect handwritten characters
https://github.com/githubharald/SimpleHTR
'''
Files = os.listdir("data/characters/")
for x in range(0, len(Files)):
    # Using a bat file to avoid issues with variable reuse in the Neural Network
    subprocess.call([r"CharacterRecognition.bat"])





