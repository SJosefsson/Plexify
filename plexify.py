"""
This is a short program that will Plexify your files for you.
Usually files have a name setup similar to:
Tv.Show.Name.SxxExx.more.text.at.the.end.fileextension

Plexify will go through a given folder and find files that
matches that name pattern and clean it up to fit Plex:
Tv Show Name - SxxExx.fileextension
"""

import os
import re

def main():
    dirPath = userInput()

    # Iterate through each file in the folder
    for filename in os.listdir(dirPath):
        # Save the old filename + path
        oldFile = os.path.join(dirPath, filename)
        # Call fileNameSearch to find and clean up filenames
        newFile = fileNameSearch(dirPath, filename)

        # Skip file that did not match regex
        if newFile == None:
            continue

        os.rename(oldFile, newFile)

def userInput():
    # Ask user to input a path to the folder where the files are
    path = input('Please paste the path to the folder where you want \
to Plexify your files.\n\
Write "." if Plexify should search in the current folder\n')

    # Tests the input to see if it's a valid folder
    while True:
        try:
            os.listdir(path)
            break
        except WindowsError:
            path = input('That\'s not a valid folder path. \
Please try again.\n')

    # Returns a valid path
    return path

def fileNameSearch(path, filename):
    """Searches the file name and checks if it matches the regex, 
       calls the cleanup function and returns the clean file name
    """

    # This namepattern will find all files named: 
    # tv.show.name.SxxExx.more.text.at.the.end.fileextension
    namepattern = re.compile(r"""^(.*?) # All text from the beginning
    ((S|s)\d\d(E|e)\d\d)                # Find SxxExx
    """, re.VERBOSE)

    found = namepattern.search(filename)
        
    # Skip file that does not match regex
    if found == None:
        return None
        
    # Clean up the file name and save it
    newFile = nameCleanup(path, found.group(1), found.group(2), filename)

    # Return path and clean file name
    return newFile

def nameCleanup(dirPath, showTitle, episodeNumber, fileEnding):
    """Clean up each part of the file name and return it"""
    
    # Clean up each part of the file name
    title = showTitle.replace('.', ' ')
    episodeNumber = '- ' + episodeNumber
    fileExtension = '.' + fileEnding.split('.')[-1]

    # Save each part of the file name as one
    fileName = title + episodeNumber + fileExtension

    # Return path and clean file name
    return os.path.join(dirPath, fileName)

if __name__ == '__main__':
    main()