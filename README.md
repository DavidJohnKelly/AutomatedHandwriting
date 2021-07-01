# Automated Handwriting
## _Convert a text file into a handwritten note_


## Features

- Import an image of a set of handwritten characters and TensorFlow will automatically assign the correct character
- Import a text file and it will generate a HTML file with your created characters with random variance where applicable


## Tech

Automated Handwriting uses a number of open source projects to work properly:

- [MyHandWriting] - creates the HTML file from the character files
- [SimpleHTR] - version of TensorFlow specifically adapted for handwritten characters
- [Pillow] - Python image manipulation capabilities

## Installation

AutomatedHandwriting requires [Python 3](https://www.python.org/downloads//) v3.8+ to run.

Install the dependencies.

```sh
pip install -r (Path)\AutomatedHandwriting\requirements.txt
```

## Usage

1. Click Browse Image Files to find the character set image 
   1a. Ensure that in the character set, each letter is roughly the same size
   1b. Ensure that each character is arranged in horizontal rows with a suitable gap left between rows. You should be able to put a finger in the gap between each row   
2. Select Start Character Analysis. TensorFlow will assign the value to each character file
   2a. You can repeat steps 1-2 for as many character sets as you like; any characters will be added without replacing existing ones
   2b. It may take a while for each character to be cropped and assigned a value, but wait until you are alerted that the process has finished 
3. Select Verify Characters to ensure that the characters were assigned the correct values
4. Click Select a Text File and find the file that you want to convert
5. Select Create a Handwritten File
   5a. The file will be saved as page.HTML. This will overwrite any existing file so ensure that if you want multiple files, you save them elsewhere first

## License

MIT

**Free to use however you want!**


   [MyHandWriting]: <https://github.com/bannyvishwas/MyHandWriting>
   [SimpleHTR]: <https://github.com/githubharald/SimpleHTR>
   [Pillow]: <https://github.com/python-pillow/Pillow>
   

