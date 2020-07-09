#!/usr/bin/env python

import os

class Ptm:

    def __init__(self):
        self.file_list = ""

    def listptmfiles(self, directory):
        #create a list of file and sub directories 
        # names in the given directory 
        listOfFile = os.listdir(directory)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(directory, entry)
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.listptmfiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

