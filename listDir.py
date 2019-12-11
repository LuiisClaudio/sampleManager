import os
import sample_db
import fato_db
from datetime import date
import smartTag
'''
    For the given path, get the List of all files in the directory tree 
'''


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def findDisk(dirPath):
    return dirPath.split('/')[2]




def read_sample(dirName):
    #dirName = '/Users/luisclaudio/Downloads/Groove Metal';

    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    # Print the files
    # for elem in listOfFiles:
    # print(elem)

    print("****************")

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    files = []#[['path', 'name', 'disk', 'extension', 'date']]
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        # files += [dirpath,[os.path.join('', file) for file in filenames]]
        for i in filenames:
            if i[-3:] in ['wav', 'mp3', 'aif']:
                files.append([i, dirpath, i[-3:], findDisk(dirpath), date.today().strftime("%d/%m/%Y") ])

    # Print the files
    # for elem in listOfFiles:
    #    print(elem)
    for elem in files:
        print(elem)
    return files

def add_sample(fileSample):
    sample_db.add(fileSample[0], fileSample[1], fileSample[2], fileSample[3], fileSample[4], )
    syncOnFato()

def add_command(lstSamples):
    for i in lstSamples[1:]:
        sample_db.add(i[0],i[1],i[2],i[3],i[4],)
    syncOnFato()

def syncOnFato():
    for row in sample_db.viewall():
        fato_db.addSampleIfNotExist(row[0])

def autoTag():
    lstAutoTag = smartTag.autoTag()
    for i in lstAutoTag:
        fato_db.addIfNotExist(i[1], i[2])

def runCode(dirName):
    minhaLista = read_sample(dirName)
    add_command(minhaLista)
    smartTag
    #autoTag()
