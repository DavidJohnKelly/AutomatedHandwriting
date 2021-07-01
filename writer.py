# Adapted from MyHandWriting by BugBoy : Github(https://github.com/bannyvishwas/MyHandWriting)
import math
import os
import random
from tkinter import messagebox

from PIL import Image


def filewrite(FilePath):
    if ".txt" in FilePath:
        htmlc = [
            "<html><head><style>.lines{width:100%;height:auto;float:left;}#paper{background:white;background-image:url('data/background.png');height:auto;float:left;padding:50px 50px;width:90%;}img,span{height:25px;width:15px;float:left;margin-top:5px;margin-bottom:10px;}.clblack{filter:brightness(30%);}.clblue{filter:brightness(100%);}</style></head><body><div id='paper'>"
        ]
        '''
        Finding the largest character image to standardise sizes
        '''
        maxHeight = 0
        maxWidth = 0
        AllCharacters = os.listdir("data/characters/")

        # Getting the max dimensions of a character in order to standardise image size
        for Character in AllCharacters:
            CharacterImage = Image.open("data/characters/" + Character)
            CharacterImage.close()

            if CharacterImage.width > maxWidth:
                maxWidth = CharacterImage.width

            if CharacterImage.height > maxHeight:
                maxHeight = CharacterImage.height

        for Character in AllCharacters:
            '''
            Capital letters added centre top
            Lowercase letters added centre middle
            p,f,g,h added centre bottom
            '''
            CharacterImage = Image.open("data/characters/" + Character)
            if CharacterImage.size != (maxHeight, maxWidth):
                NewImage = Image.new("RGBA", (maxWidth, maxHeight), (255, 255, 255, 0))

                x = int(math.floor((maxWidth - CharacterImage.width) / 2))
                y = 0

                if Character.islower() and Character != "p" and Character != "f" and Character != "g" and Character != "j":
                    y = int(math.floor((maxHeight - CharacterImage.height) / 2))

                if Character == "p" or Character == "f" or Character == "g" or Character == "j":
                    y = int(math.floor((maxHeight - CharacterImage.height) / 2)) * 2

                NewImage.paste(CharacterImage, (x, y, x + CharacterImage.width, y + CharacterImage.height))
                CharacterImage.close()
                # Clears redundant files
                os.remove("data/characters/" + Character)
                NewImage.save("data/characters/" + Character)

        '''
        Appending each character to the HTML file
        '''
        with open(FilePath, "r") as textfile:
            for line in textfile:
                # Strips the newline character
                curst = line.replace("\\n", "")
                htmlc.append('<div class="lines">')
                for ch in curst:

                    # get char ASCII Code of char
                    chcode = ord(ch)
                    if chcode == 32 or chcode == 36:
                        htmlc.append("<span></span>")

                    if chcode != 32 and chcode != 10:
                        print(chcode, ch)
                        SpecificCharacter = []

                        for Character in AllCharacters:
                            if ch in Character.replace("png", "").replace(".", ""):
                                SpecificCharacter.append(Character)
                        try:
                            # Randomising character selection if multiple options available
                            RandomCharacter = random.choice(SpecificCharacter)
                            htmlc.append(
                                "<img src='data/characters/{}'/>".format(RandomCharacter)
                            )
                        except IndexError:
                            messagebox.showinfo("Error!", " {} doesn't exist in Character Set".format(ch))

                htmlc.append("</div>")

        htmlc.append("</div></body></html>")

        with open("page.html", "w") as page_html:
            page_html.writelines(htmlc)
