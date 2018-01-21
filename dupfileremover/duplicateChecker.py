#!/usr/bin/python3

import os
import sys
import hashlib

# the compileFiles function takes in an argument(path) and uses that to find all
# files wihtin that path. Those are the files that will be hashed to check for
# duplicates.


def compileFiles(path):

    # the list that will store the absolute path the each file found

    file = []

    # this forloop breaks down that path that is passed in, into 3 parts.
    # root (the absolute path leading up to the folder)
    # dirs (to find all other dirs in the path, not used here)
    # files(these are the files that are found)
    # after finding all files the root is appened to the file and then stored
    # in the file list

    for root, dirs, files in os.walk(path):
        for name in files:
            file.append(os.path.join(root, name))
    return file

# the hashFiles function takes in a single argument (fileList) which is a list.
# This list contains the absolute path of all the files that are to be hashed


def hashFiles(fileList):

    # the dictionary that stores all the results

    results = {}

    # this forloop goes through each entry in the fileList. The name of the file
    # (that is the absolute path name) is saved in the variable "name", then the
    # file is opened and an md5 hash is calculated on it. You need to have the
    # absolute filepath for the hash to calculate properly. When the hash is
    # calculated it checks to see if the same hash is already found in the
    # results dict using the hash value as the key. If the same hash is already
    # found in the results dict then the new name is appended onto the end of
    # the names list for each md5sum found. If the md5sum is not in the results
    # dict, then the md5sum is added as they key, and a list is created as the
    # value, with the name being added as the first value

    print("Hashing the files now...")
    for name in fileList:
        with open(name, "rb") as aFile:
            fileContents = aFile.read()
            value = hashlib.md5(fileContents).hexdigest()
        if value in results:
            results[value].append(name)
        else:
            results[value] = [name]
    return results

# the save results function takes in a results parameter which is a dictionary
# the functions opens a text file called "output.txt" then chechs the results
# dict. Using the md5sum as they key, and the names of the absolute paths as the
# values, a for loop checks to see if there are more than 2 name matches
# if there are more than 2 name matches a line is written with the md5sum, and
# the absolute paths of each of the corresponding duplicate files for that md5sum


def saveResults(results, maxNumDupsWanted):
    print("Saving the hashes...")
    with open("duplicates.txt", "w") as textFile:
        for k, v in results.items():
            if(len(v) > maxNumDupsWanted):
                textFile.write("----MD5sum: {}----\n".format(k))
                count = len(v)
                for i in v:
                    if(count > 1):
                        textFile.write("{}\n".format(i))
                    else:
                        textFile.write("{}\n\n".format(i))
                    count -= 1
    print("Done!")


if __name__ == "__main__":
    if(len(sys.argv) > 2):
        # this variable is used to store all the files that will be passed to
        # the different fucntions later

        fileList = []

        # numOfDups is used to see how many of the same file should be taken
        # into account when searching. If you don't want more than 1 of the
        # same file, then you would enter 1. If you are expecting to have
        # multiple duplicates, then you would enter in the maximum number of a
        # file you are willing to have. You want to put in the maximum number of
        # duplicates you are fine with finding

        try:
            numOfDups = sys.argv[1]
            numOfDups = int(numOfDups)

        except ValueError:
            print("Sorry, but the second input has to be a whole number")

        # the folders variable takes in all the folders that wish to be searched
        # and stores them in a list. Then that list is passed to the compileFiles
        # function, and the results are returned and appened to the fileList
        # variable to create one master list. if a folder entered does not exits
        # it prints an error message to the screen and continues

        folders = sys.argv[2:]

        print("Compiling all files into the master list...")
        for i in folders:
            if(os.path.isdir(i) is True):
                fileList.append(compileFiles(i))

            elif(os.path.isdir(i) is False):
                print("\nSorry, but it seems like '{}' is not a folder\n".format(i))

        # after all the files have been compiled into the fileList variable,
        # there are many lists nested within lists. This list comprehension
        # unpacks all of the values of all lists into only one list to avoid
        # issues with the hashFiles function

        flattened = [val for sublist in fileList for val in sublist]
        results = hashFiles(flattened)

        saveResults(results, numOfDups)

    else:
        print("Not enough arguments. you need to enter in the maximum number",
              "of duplicate files you are willing to find, then paths to",
              "folder(s). Ex: python test.py 1 path/to/folder1 path/folder2")
