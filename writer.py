# Adapted from MyHandWriting by BugBoy : Github(https://github.com/bannyvishwas2020)
import math
import random
import os
from PIL import Image

htmlc = [
    "<html><head><style>.lines{width:100%;height:auto;float:left;}#paper{background:white;background-image:url('data/background.png');height:auto;float:left;padding:50px 50px;width:90%;}img,span{height:25px;width:15px;float:left;margin-top:5px;margin-bottom:10px;}.clblack{filter:brightness(30%);}.clblue{filter:brightness(100%);}</style></head><body><div id='paper'>"
]

maxHeight = 0
maxWidth = 0
AllCharacters = os.listdir("data/characters/")

# Getting the max dimensions of a character in order to standardise image size
for Character in AllCharacters:
    CharacterImage = Image.open("data/characters/" + Character)
    CharacterImage.close()
    print(str(CharacterImage.width) + " x " + str(CharacterImage.height))
    if CharacterImage.width > maxWidth:
        maxWidth = CharacterImage.width
        print("BIGGER WIDTH")

    if CharacterImage.height > maxHeight:
        maxHeight = CharacterImage.height
        print("BIGGER HEIGHT")

for Character in AllCharacters:
    CharacterImage = Image.open("data/characters/" + Character)
    if CharacterImage.width != maxWidth and CharacterImage.height != maxHeight:
        NewImage = Image.new("RGBA", (maxWidth, maxHeight), (255, 255, 255, 0))
        x1 = int(math.floor((maxWidth - CharacterImage.width) / 2))
        y1 = int(math.floor((maxHeight - CharacterImage.height) / 2))

        NewImage.paste(CharacterImage, (x1, y1, x1 + CharacterImage.width, y1 + CharacterImage.height))
        CharacterImage.close()
        os.remove("data/characters/" + Character)
        NewImage.save("data/characters/" + Character)

with open("content.txt", "r") as textfile:
    for line in textfile:
        # Strips the newline character
        curst = line.strip()
        htmlc.append('<div class="lines">')
        for ch in curst:

            # get char ASCII Code of char
            chcode = ord(ch)

            if chcode == 32 or chcode == 36:
                htmlc.append("<span></span>")

            if chcode != 32:

                SpecificCharacter = []

                for Character in AllCharacters:

                    if ch in Character.replace(".png", ""):
                        SpecificCharacter.append(Character)

                RandomCharacter = random.choice(SpecificCharacter)

                htmlc.append(
                    "<img src='data/characters/{}'/>".format(RandomCharacter)
                )
        htmlc.append("</div>")

htmlc.append("</div></body></html>")

with open("page.html", "w") as page_html:
    page_html.writelines(htmlc)
