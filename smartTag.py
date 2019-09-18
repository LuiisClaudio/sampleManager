import os
import tag_db
import fato_db
from datetime import date
import indexs


def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def autoTag():
    lstTag = []

    #tagFromFile
    f = open('autoTag.txt',"r")
    lines = f.readlines()
    for i in lines:
        lstTag.append(i.split(" ")[0].replace("\n", ""))

    #Key
    lstKey = ['C','D','E','F','G','A','B','C#','D#','F#','G#','A#','Cmin','Dmin','Emin','Fmin','Gmin','Amin','Bmin','C#min','D#min','F#min','G#min','A#min']
    lstKey = sorted(lstKey)
    for i in lstKey:
        lstTag.append(' ' + i + '_')
        lstTag.append('_' + i + ' ')
        lstTag.append('_' + i + '_')
        lstTag.append(' ' + i + ' ')

    lstTagDB = scanTagsBasic('LevantamentoDeTagsPadrao/')
    for i in lstTagDB:
        lstTag.append(i[0])
        #for k in i[1]:
        #    lstTag.append(k)
    # bpm
    for i in range(1, 300):
        lstTag.append(str(i))

    #search
    tagTable = []
    tagTableAux = tag_db.viewall()
    for i in tagTableAux:
        for k in lstTagDB:
            if i[1] == k[0]:
                tagTable.append(i)

    # lookup operation
    fatoTable = fato_db.selectAll()
    lstAddTag = []
    for i in fatoTable:
        for k in tagTable:
            if (i[2].find(k[1]) != -1 and k[1] != '') and (k[1] not in lstKey):
                print(i[0], i[2], '-----------',k[0], k[1])
                lstAddTag.append([i[0],i[1],k[0]])
    #print(sample_row)
    #print(lstTag)
    return lstAddTag
    
    

def fillKey():
    lst =  ['C','D','E','F','G','A','B','C#','D#','F#','G#','A#','Cmin','Dmin','Emin','Fmin','Gmin','Amin','Bmin','C#min','D#min','F#min','G#min','A#min']
    for i in lst:
        tag_db.addIfNotExist(i, date.today().strftime("%d/%m/%Y"))

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




def scanTags(dirName):
    #dirName = '/Users/luisclaudio/Downloads/Groove Metal';


    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)
    #print(listOfFiles)

    # Print the files
    # for elem in listOfFiles:
    # print(elem)

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    files = []  # [['path', 'name', 'disk', 'extension', 'date']]
    interessa = []
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        #print(dirpath, dirnames)
        if dirnames != []:
            #print([dirpath.split('/')[-1], dirnames])
            interessa.append([dirpath.split('/')[-1], dirnames])
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        files += [dirpath]
        for i in filenames:
            files.append(dirpath)


    #for elem in listOfFiles:
    #    print(elem)

    #for i in files:
    #    print(i)
    return interessa

def scanTagsBasic(dirName):


    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    files = []  # [['path', 'name', 'disk', 'extension', 'date']]
    interessa = []
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        #print(dirpath, dirnames)
        if dirnames != []:
            #print([dirpath.split('/')[-1], dirnames])
            interessa.append([dirpath.split('/')[-1]])
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        files += [dirpath]
        for i in filenames:
            files.append(dirpath)


    #for elem in listOfFiles:
    #    print(elem)

    #for i in files:
    #    print(i)
    return interessa

def fillSampleTagBasic(lst):
    for tag_lst in lst:
        for tag_name in tag_lst:
            #print(tag_name.replace(" ", ""), date.today().strftime("%d/%m/%Y"))
            tag_db.addIfNotExist(tag_name.replace(" ", ""), date.today().strftime("%d/%m/%Y"))

def fillSampleTag(lst):
    for tag_lst in lst:
        #print(tag_lst[0].replace(" ", ""), date.today().strftime("%d/%m/%Y"))
        tag_db.addIfNotExist(tag_lst[0].replace(" ", ""), date.today().strftime("%d/%m/%Y"))
    for tag_lst in lst:
        for tag_name in tag_lst[1]:
            tag_db.addIfNotExist((tag_name).replace(" ", ""), date.today().strftime("%d/%m/%Y"))
            #print((tag_lst[0] + '->' + tag_name).replace(" ", ""), date.today().strftime("%d/%m/%Y"))
            #tag_db.addIfNotExist((tag_lst[0] + '_' + tag_name).replace(" ", ""), date.today().strftime("%d/%m/%Y"))
            if tag_lst[0] != '':
                tag_db.addIfNotExist((tag_lst[0] + '->' + tag_name).replace(" ", ""), date.today().strftime("%d/%m/%Y"))
            else:
                tag_db.addIfNotExist((tag_name).replace(" ", ""), date.today().strftime("%d/%m/%Y"))

def runCode(dirName):
    minhaLista = scanTags(dirName)
    fillSampleTag(minhaLista[1:])
    fillKey()


def searchTag():
    return
runCode(indexs.tagSamplesDescDir)
#autoTag()