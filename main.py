import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from writer import filewrite
from PIL import Image, ImageFilter, ImageTk

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


def main(filepath):
    originalpicture = Image.open(filepath)
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
    Counter = 0
    for item in Files:
        croplist = []
        if "HorizontalCrop" in item:
            Counter = Counter + 1
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
                "data/characters/Cropped{}.png".format(Counter))
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
    for file in Files:
        if "Cropped" in file:
            # Using a bat file to avoid issues with variable reuse in the Neural Network
            subprocess.call([r"CharacterRecognition.bat"])


CharacterCounter = 0


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.filepath = ""
        self.start()

    def callback(self):
        self.root.quit()

    def getFilePath(self):
        return self.filepath

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title("Automated Handwriting")
        # Create a File Explorer label
        label_file_explorer = tk.Label(self.root,
                                       text="Select a character set",
                                       width=100, height=4,
                                       fg="blue")
        label_file_explorer.pack()

        def getCharacterSet():
            return os.listdir("data/characters/")

        # Function for opening the file explorer window
        def browseImageFiles():
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select a Character Set",
                                                  filetypes=(("PNG Files",
                                                              "*.png*"),
                                                             ("JPEG Files",
                                                              "*.jpeg*")
                                                             ))

            # Change label contents
            label_file_explorer.configure(text="File Opened: " + os.path.abspath(filename))

        def browseTextFiles():
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select a Character Set",
                                                  filetypes=(("TXT Files",
                                                              "*.txt*"),
                                                             ))

            # Change label contents
            label_file_explorer.configure(text="File Opened: " + os.path.abspath(filename))

        def startMain():
            if ".png" in label_file_explorer.cget("text") or ".jpeg" in label_file_explorer.cget("text"):
                self.filepath = label_file_explorer.cget("text").replace("File Opened: ", "")
                th = threading.Thread(target=startAnalysis())
                th.start()

        def initialiseCharacterVerification():
            global CharacterCounter
            CharacterCounter = 0
            CharacterSet = getCharacterSet()

            '''
                Updates the character image and text for each character after confirm is pressed
            '''
            def updateWindow(Set):
                global CharacterCounter

                try:
                    os.rename("data/characters/" + Set[CharacterCounter],
                              "data/characters/" + CharacterInput.get("1.0", "end-1c") + ".png")
                except IOError:
                    NewFile = False
                    Counter = 1
                    while not NewFile:
                        try:
                            os.rename("data/characters/" + Set[CharacterCounter],
                                      "data/characters/{}{}.png".format(CharacterInput.get("1.0", "end-1c"),
                                                                        "." * Counter))
                            NewFile = True
                        except IOError:
                            Counter = Counter + 1

                CharacterCounter = CharacterCounter + 1
                if CharacterCounter < len(CharacterSet):
                    newImage = Set[CharacterCounter]
                    newCharacterImage = ImageTk.PhotoImage(Image.open("data/characters/" + newImage))
                    CharacterPanel.configure(image=newCharacterImage)
                    CharacterPanel.image = newCharacterImage
                    CharacterInput.delete("1.0", "end")
                    CharacterInput.insert("1.0", newImage.replace(".", "").replace("png", ""))
                else:
                    messagebox.showinfo("ALERT", "All character verified")
                    CharacterWindow.destroy()


            '''
                Creating a separate window for the character verification process
            '''
            CharacterWindow = tk.Toplevel()
            CharacterImage = ImageTk.PhotoImage(Image.open("data/characters/" + CharacterSet[0]))
            CharacterPanel = tk.Label(CharacterWindow, image=CharacterImage)
            CharacterPanel.image = CharacterImage

            CharacterLabel = tk.Label(CharacterWindow, text="This character is: ")
            CharacterInput = tk.Text(CharacterWindow, height=1, width=5)
            CharacterInput.insert("1.0", CharacterSet[0].replace(".", "").replace("png", ""))

            ConfirmButton = tk.Button(CharacterWindow, text="Confirm", command=lambda: updateWindow(CharacterSet))
            CharacterLabel.grid(column=2, row=2)
            CharacterPanel.grid(column=2, row=1)
            CharacterInput.grid(column=3, row=2)
            ConfirmButton.grid(column=4, row=2)

        button_explore = tk.Button(self.root,
                                   text="Browse Image Files",
                                   command=browseImageFiles)

        button_start = tk.Button(self.root,
                                 text="Start Character Analysis",
                                 command=startMain)

        button_verify = tk.Button(self.root,
                                  text="Verify Characters",
                                  command=initialiseCharacterVerification)

        button_content = tk.Button(self.root,
                                   text="Select a Text File",
                                   command=browseTextFiles)

        button_CreateFile = tk.Button(self.root,
                                      text="Create a Handwritten File",
                                      command=lambda: filewrite(
                                          label_file_explorer.cget("text").replace("File Opened: ", "")))

        button_exit = tk.Button(self.root,
                                text="Exit",
                                command=exit)

        '''Grid method is chosen for placing
        the widgets at respective positions
        in a table like structure by
        specifying rows and columns'''
        label_file_explorer.grid(column=1, row=1)

        button_explore.grid(column=1, row=2)
        button_start.grid(column=1, row=3)
        button_verify.grid(column=1, row=4)
        button_content.grid(column=1, row=5)
        button_CreateFile.grid(column=1, row=6)
        button_exit.grid(column=1, row=7)

        # Let the window wait for any events
        self.root.mainloop()


# Created separate threads to prevent application freezing whilst character analysis is ongoing
app = App()


def startAnalysis():
    messagebox.showinfo("ALERT",
                        "The character analysis is now running. Do not close it, edit any files, or click any "
                        "other buttons. You will be alerted when the analysis process has completed.")
    Started = False
    while not Started:
        FilePath = app.getFilePath()
        if FilePath != "":
            print("Started")
            main(FilePath)
            Started = True
    messagebox.showinfo("ALERT",
                        "The character analysis has finished running, continue with the use of the application")
