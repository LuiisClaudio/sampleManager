from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import sample_db
import tag_db
import fato_db
import listDir
import smartTag
from datetime import date
import indexs
import MusicPlayer
import audio_metadata
import time
import moreInfoSamplePage


class samplePage:

    def __init__(self):
        self.window = Tk()
        self.window.title("Manage Sample")
        self.window.geometry("1920x1080")
        #self.window.resizable(0, 0)

        self.samplePlayer = MusicPlayer.Teste()

        self.treeRowValue = []
        self.selectedSample = None

        self.loopMode = False
        self.isPausedStatus = False

        directory = 'D:\\'

        self.factQuery = []
        self.tagQuery = []

        self.t = StringVar()
        self.t.set("00:00")

        self.label = tk.Label(text="")
        self.label.place(x=300 + indexs.xPlayerGrid,y=300 + indexs.yPlayerGrid)
        self.update_clock()


        self._buildMenuBar()

        self._buildSampleSpace()

        self._buildTagSpace()

        self._buildPlayerSpace()

        self.window.mainloop()

    def viewInfoSample(self):
        self.newWindow = tk.Toplevel(self.window)
        self.app = moreInfoSamplePage.SampleInfo(self.newWindow)

    def _buildMenuBar(self):
        menubar = Menu(self.window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.abreFaixasDir)
        #filemenu.add_command(label="Open", command=self.abreFaixasDir)
        menubar.add_cascade(label="Folder", menu=filemenu)
        self.window.config(menu=menubar)

    def _buildSampleSpace(self):

        self._create_treeview()

        Label(self.window, text="Sample").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid)
        self.sampleSearch = StringVar()
        # self.sampleSearch.set("Name")
        Entry(self.window, textvariable=self.sampleSearch, width=10).place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid)

        Label(self.window, text="Tag").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 1))
        self.tagSearch = StringVar()
        Entry(self.window, textvariable=self.tagSearch, width=10).place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 1))

        Label(self.window, text="Path").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 2))
        self.pathSearch = StringVar()
        # self.pathSearch.set("Name")
        Entry(self.window, textvariable=self.pathSearch, width=10).place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 2))

        Label(self.window, text="BPM").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 3))
        self.bpmSearch = ttk.Spinbox(self.window, values=indexs.lstBpm, width=3)
        self.bpmSearch.place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 3))

        Label(self.window, text="Key").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 4))
        self.keySearch = ttk.Combobox(self.window, values=indexs.lstKey, width=5)
        self.keySearch.place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 4))

        Label(self.window, text="Genre").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 5))
        self.genreSearch = ttk.Combobox(self.window, values=indexs.lstGenre, width=10)
        self.genreSearch.place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 5))

        Label(self.window, text="LoveLow").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 6))
        self.loveLowSearch = ttk.Spinbox(self.window, values=indexs.lstLove, width=3)
        self.loveLowSearch.place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 6))

        Label(self.window, text="Love Upper").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 7))
        self.loveUpperSearch = ttk.Spinbox(self.window, values=indexs.lstLove, width=3)
        self.loveUpperSearch.place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 7))

        Label(self.window, text="Extension").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 8))
        self.extensionSearch = StringVar()
        # self.extensionSearch.set("Name")
        Entry(self.window, textvariable=self.extensionSearch, width=10).place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 8))

        Label(self.window, text="Disk").place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 9))
        self.diskSearch = StringVar()
        # self.diskSearch.set("Name")
        Entry(self.window, textvariable=self.diskSearch, width=10).place(x=indexs.xSearchGrid + indexs.spaceSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 9))

        Button(self.window, text='Search', bd=2, font=('arialblack', 13), width=5, command=self.search_command).place(x = indexs.xSearchGrid, y = indexs.ySearchGrid + (indexs.padSearchGrid * 10))
        Button(self.window, text='Clear All', bd=2, font=('arialblack', 13), width=5, command=self.clearAllSearch).place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 11))


        Button(self.window, text='Save', bd=2, font=('arialblack', 13), width=5, command=self.editSampleInfo).place(
            x=indexs.xSearchGrid, y=550)
        # Button(self.window, text='Details', bd=2, font=('arialblack', 13), width=5, command=self.viewInfoSample).place(x=520, y=550)
        Button(self.window, text='Delete', bd=2, font=('arialblack', 13), width=5, command=self.deleteSample).place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 12))
        Button(self.window, text='Hard Delete', bd=2, font=('arialblack', 13), width=9,
               command=self.hardDeleteSample).place(x=indexs.xSearchGrid, y=indexs.ySearchGrid + (indexs.padSearchGrid * 13))

        Label(self.window, text="Name").place(x=indexs.xSearchGrid, y=550)
        Label(self.window, text="Tag").place(x=indexs.xSearchGrid, y=600)  # .place(x=10, y=750)
        Label(self.window, text="BPM").place(x=indexs.xSearchGrid, y=650)#.place(x=10, y=600)
        Label(self.window, text="Key").place(x=indexs.xSearchGrid, y=700)#.place(x=10, y=650)
        Label(self.window, text="Genre").place(x=indexs.xSearchGrid, y=750)#.place(x=10, y=700)
        Label(self.window, text="Love").place(x=indexs.xSearchGrid, y=800)


        self.editSampleName =  Label(self.window, text="-")
        self.editSampleName.place(x=100, y=550)

        self.tagListComboBox = []
        #for i in tag_db.viewallNames():
        #    self.tagListComboBox.append(i[0])
        #self.editSampleTag = ttk.Combobox(self.window, values=self.tagListComboBox)
        #self.editSampleTag.place(x=100, y=600)#.place(x=100, y=750)
        self.editTagNameVar = StringVar()
        self.editTagName = Label(self.window, text="-", textvariable=self.editTagNameVar)
        self.editTagName.place(x=100, y=600)


        self.editSampleBpm = ttk.Spinbox(self.window, values=indexs.lstBpm, width=3)
        self.editSampleBpm.place(x=100, y=650)#.place(x=100, y=600)

        self.box_value = StringVar()
        self.editSampleKey = ttk.Combobox(self.window, textvariable=self.box_value, values=indexs.lstKey, state='readonly', width=5)
        self.editSampleKey.place(x=100, y=700)#.place(x=100, y=650)

        self.editSampleGenre = ttk.Combobox(self.window, values=indexs.lstGenre, width=10)
        self.editSampleGenre.place(x=100, y=750)#.place(x=100, y=700)


        self.editSampleLove = ttk.Spinbox(self.window, values=indexs.lstLove, width=10)
        self.editSampleLove.place(x=100, y=800)


    def _create_treeview(self):
        self.dataCols = ["Index", "Sample", "Tag", "Path", "Extension", "Disk", "BPM", "Key", "Genre", "Love"]  # ['name', 'path', 'extension']
        self.tree = ttk.Treeview(self.window, columns=self.dataCols, show='headings', height = 25)
        self.tree.place(x = indexs.xTree, y = indexs.yTree)
        self.tree.bind('<ButtonRelease-1>', self.selectTreeValues)
        self.tree.bind('<Up>', self.selectTreeValuesKey)
        self.tree.bind('<Down>', self.selectTreeValuesKey)

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.xview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # add tree and scrollbars to frame
        #ysb.grid(in_=self.window, row=10, column=1, columnspan=6)
        #xsb.grid(in_=self.window, row=11, column=2, columnspan=6)

        self.tree["displaycolumns"] = self.dataCols

        self._load_data()


    def _load_data(self):
        # add data to the tree
        self.indexSample = 0
        self.factQuery = fato_db.selectAll()
        cont = 1
        for item in self.factQuery:
            self.insertTreeData(cont, [item[2], item[7], item[3], item[4], item[5], item[8], item[9], item[10], item[11]])
            cont = cont + 1


        self.tree.column('Index', width=35, minwidth=35)
        self.tree.column('Sample', width=200, minwidth=200)
        self.tree.column('Tag', width=200, minwidth=200)
        self.tree.column('Path', width=200, minwidth=200)
        self.tree.column('Extension', width=30, minwidth=30)
        self.tree.column('Disk', width=30, minwidth=30)
        self.tree.column('BPM', width=35, minwidth=35)
        self.tree.column('Key', width=35, minwidth=35)
        self.tree.column('Genre', width=200, minwidth=200)
        self.tree.column('Love', width=35, minwidth=35)

        self.tree.tag_configure('zero', background='orange', foreground="black")
        self.tree.tag_configure('vinte', background='dark orange', foreground="black")
        self.tree.tag_configure('quarenta', background='coral', foreground="black")
        self.tree.tag_configure('sessenta', background='tomato', foreground="black")
        self.tree.tag_configure('oitenta', background='red', foreground="black")
        self.tree.tag_configure('cem', background='green2', foreground="black")
        self.tree.tag_configure('unview', background='white', foreground="black")
        ttk.Style().configure("Treeview", background="#383838",
                              foreground="IndianRed", fieldbackground="white")

    def insertTreeData(self, cont, item):
        #for i in range(len(item)):
        #    if item[i] == None:
        #        item[i] = '-'
        loveValue = item[8]
        if loveValue != 'None' and loveValue != '' and loveValue != 'NULL':
            if loveValue != None:
                if int(item[8]) < 20:
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]], tags = ('zero',))
                elif int(item[8]) < 40:
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]], tags=('vinte',))
                elif int(item[8]) < 60:
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]], tags=('quarenta',))
                elif int(item[8]) < 80:
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]], tags=('sessenta',))
                elif int(item[8]) < 100:
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]], tags=('oitenta',))
                elif int(item[8]) == 100:
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]], tags=('cem',))
            else:
                if item[1] == '-':
                    self.tree.insert('', 'end',
                                     values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6],
                                             item[7], item[8]], tags=('unview',))
                else:
                    self.tree.insert('', 'end', values=[cont, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]])

    def selectTreeValues(self, event):
        curItem = self.tree.focus()
        treeValue = self.tree.item(curItem)
        self.treeRowValue = treeValue['values']
        print('-->',self.treeRowValue)
        self.indexSample = self.treeRowValue[0] - 1
        self.changeSelectedSample()
        self.fillSampleInfo()
        self.audioMetaData()

    def changeFocus(self, val):
        if self.treeRowValue != []:
            curItem = self.tree.focus()
            print(curItem)
            curItem = curItem.replace('I', '0x')
            print(curItem)
            print(int(curItem, 16))
            curItem = int(curItem, 16) + val
            curItem = hex(curItem)
            curItem = str(curItem).upper().replace('X', '')
            print(curItem)
            if len(curItem) == 1:
                curItem = 'I00' + curItem
            if len(curItem) == 2:
                curItem = 'I0' + curItem
            if len(curItem) == 3:
                curItem = 'I0' + curItem[1:]
            else:
                curItem = 'I' + curItem[1:]
            print(curItem)
            return curItem


    def selectTreeValuesKey(self, event):
        #print(event.keycode)
        def detectKey(key):
            if key.keycode == 8255233 or key.keycode == 8192084:
                return 1
            elif key.keycode == 8320768 or key.keycode == 8257618:
                return -1
        curItem = self.changeFocus(detectKey(event))
        treeValue = self.tree.item(curItem)
        self.treeRowValue = treeValue['values']
        print('-->',self.treeRowValue)
        self.indexSample = self.treeRowValue[0] - 1
        self.changeSelectedSample()
        self.fillSampleInfo()
        self.audioMetaData()

    def changeSelectedSample(self):
        if self.treeRowValue != []:
            self.selectedSample = self.treeRowValue[3] + '/' + self.treeRowValue[1]
            self.samplePlayer.changeSample(self.selectedSample)

    def fillSampleInfo(self):
        def searchIndexTag(name):
            found = False
            for position in (x for x, n in enumerate(self.tagListComboBox) if n == name):
                self.tagListComboBox[position]
                return position
            if not found:
                return 0

        if self.treeRowValue[indexs.selectedTreeSample] != None and self.treeRowValue[indexs.selectedTreeSample] != 'None' and self.treeRowValue[indexs.selectedTreeSample] != '':
            self.editSampleName['text'] = self.treeRowValue[indexs.selectedTreeSample]
        else:
            self.editSampleName['text'] = '-'

        if self.treeRowValue[indexs.selectedTreeTag] != None and self.treeRowValue[indexs.selectedTreeTag] != 'None' and self.treeRowValue[indexs.selectedTreeTag] != '-':
            self.editTagNameVar.set(self.treeRowValue[indexs.selectedTreeTag])
        else:
            self.editTagNameVar.set('-')

        #self.editSampleKey.current(indexs.lstKey.index(self.treeRowValue[indexs.selectedTreeKey]))

        #if self.treeRowValue[indexs.selectedTreeTag] != None and self.treeRowValue[indexs.selectedTreeTag] != 'None':
        #    self.editSampleTag.current(searchIndexTag(self.treeRowValue[indexs.selectedTreeTag]))

        if self.treeRowValue[indexs.selectedTreeBpm] != None and self.treeRowValue[indexs.selectedTreeBpm] != 'None' and self.treeRowValue[indexs.selectedTreeBpm] != '':
            self.editSampleBpm.set(self.treeRowValue[indexs.selectedTreeBpm])
        else:
            self.editSampleBpm.set('')

        if self.treeRowValue[indexs.selectedTreeKey] != None and self.treeRowValue[indexs.selectedTreeKey] != 'None' and self.treeRowValue[indexs.selectedTreeKey] != '':
            print(self.treeRowValue[indexs.selectedTreeKey])
            self.editSampleKey.current(indexs.lstKey.index(self.treeRowValue[indexs.selectedTreeKey]))
        else:
            self.editSampleKey.set('')

        if self.treeRowValue[indexs.selectedTreeGenre] != None and self.treeRowValue[indexs.selectedTreeGenre] != 'None' and self.treeRowValue[indexs.selectedTreeGenre] != '':
            self.editSampleGenre.current(indexs.lstGenre.index(self.treeRowValue[indexs.selectedTreeGenre]))
        else:
            self.editSampleGenre.set('')

        if self.treeRowValue[indexs.selectedTreeLove] != None and self.treeRowValue[indexs.selectedTreeLove] != 'None' and self.treeRowValue[indexs.selectedTreeLove] != '':
            self.editSampleLove.set(self.treeRowValue[indexs.selectedTreeLove])
        else:
            self.editSampleLove.set('')

    def editSampleInfo(self):
        def searchIdTag(name):
            print(name)
            if name != None and name != '' and name != '-':
                return tag_db.findTagId(name)
            else:
                return None

        print(self.factQuery[self.treeRowValue[indexs.selectedTreeCount] - 1])
        id_fato = self.factQuery[self.treeRowValue[indexs.selectedTreeCount] - 1][indexs.fatoQueryIdFato]
        love = self.editSampleLove.get()
        id_tag = searchIdTag(self.editTagNameVar.get())
        id_sample = self.factQuery[self.treeRowValue[indexs.selectedTreeCount] - 1][indexs.fatoQueryIdSample]
        print(id_fato, love, id_tag)
        fato_db.updateByInterface(id_fato, id_sample, love, id_tag)


        bpm = self.editSampleBpm.get()
        key = self.editSampleKey.get()
        genre = self.editSampleGenre.get()
        print(id_sample, bpm, key, genre)
        sample_db.updateByInterface(id_sample, bpm, key, genre)

        self.refresh()

    def deleteSample(self):
        deleteRowFact = self.factQuery[self.indexSample]
        fato_db.delete(deleteRowFact[indexs.fatoQueryIdFato])
        sample_db.delete(deleteRowFact[indexs.fatoQueryIdSample])

        self.refresh()

    def hardDeleteSample(self):
        self.search_command()
        for deleteRow in self.factQuery:
            print(deleteRow)
            fato_db.delete(deleteRow[indexs.fatoQueryIdFato])
            sample_db.delete(deleteRow[indexs.fatoQueryIdSample])
        self.search_command()

    def clearAllSearch(self):
        self.sampleSearch.set('')
        self.pathSearch.set('')
        self.extensionSearch.set('')
        self.diskSearch.set('')
        self.bpmSearch.set('')
        self.keySearch.set('')
        self.genreSearch.set('')
        self.tagSearch.set('')

        self.loveLowSearch.set('')
        self.loveUpperSearch.set('')


    def _buildTagSpace(self):
        value = StringVar()
        self.modeTagQuery = ttk.Combobox(self.window, values=['Name', 'Most Used', 'Last Used'], width = 10, state='readonly')
        self.modeTagQuery.place(x = indexs.xTagGrid, y = indexs.yTagGrid - 30)
        self.modeTagQuery.current(0)
        self._createListTag()

        Button(self.window, text='Add', bd=2, font=('arialblack', 13), width=5, command=self.addTag).place(x=indexs.xTagGrid + indexs.padTagGrig, y=indexs.yTagGrid)
        Button(self.window, text='Remove', bd=2, font=('arialblack', 13), width=5, command=self.removeTag).place(x=indexs.xTagGrid+ indexs.padTagGrig + 60, y=indexs.yTagGrid )
        #Button(self.window, text='Edit', bd=2, font=('arialblack', 13), width=5, command='').place(x=indexs.xTagGrid + 120, y=10)

        self.tagNameEdit = StringVar()
        self.tagNameEditEntry = Entry(self.window, textvariable=self.tagNameEdit, width=10)
        self.tagNameEditEntry.place(x=indexs.xTagGrid + indexs.padTagGrig, y=indexs.yTagGrid-30)
        Button(self.window, text='Search', bd=2, font=('arialblack', 13), width=5, command=self.searchTagByName).place(x=indexs.xTagGrid + 120, y=indexs.yTagGrid )

        self.tagSearchNameEntry = StringVar()
        #self.tagSearch.set("Name")
        Entry(self.window, textvariable=self.tagSearchNameEntry, width=12).place(x=indexs.xTagGrid, y=indexs.yTagGrid)

        Button(self.window, text="Sync Tag", width=12, command=self.syncTag).place(x=indexs.xTagGrid  + (indexs.padTagGrig*3) - 90, y=indexs.yTagGrid + 30)
        Button(self.window, text="Untag", width=12, command=self.untag).place(x=indexs.xTagGrid + (indexs.padTagGrig*3) - 90, y=indexs.yTagGrid + 80)

    def _createListTag(self):
        self.tagListbox = Listbox(self.window, height=15, width=55)
        self.tagListbox.place(x = indexs.xTagGrid, y = indexs.yTagGrid + 30)
        self.indexTag = 0

        sb = Scrollbar(self.window)
        #sb.grid(row=1, column=2, rowspan=6)

        self.tagListbox.configure(yscrollcommand=sb.set)
        sb.configure(command=self.tagListbox.yview)

        self.tagListbox.bind('<<ListboxSelect>>', self.getSelectedRow)
        self.view_command()

    def getSelectedRow(self, event):
        try:
            #indexSampleAnt = self.indexSample
            self.indexTag = self.tagListbox.curselection()[0]
            selectedTuple = self.tagListbox.get(self.indexTag)
            print(self.indexTag, selectedTuple)
            #self.tagListbox.itemconfig(self.indexSample, bg='pale turquoise', fg='black')
            #self.tagListbox.itemconfig(indexSampleAnt, bg='white', fg='black')
            self.tagNameEdit.set(selectedTuple)


        except IndexError:
            pass

    def searchTagByName(self):
        def sendOrderBy():
            if self.modeTagQuery.get() == 'Name':
                return 'Name'
            elif self.modeTagQuery.get()==  'Most Used':
                return 'Most'
            elif self.modeTagQuery.get()== 'Last Used':
                return 'Last'
            else:
                return 'Name'
        self.tagQuery = tag_db.search(self.tagSearchNameEntry.get(), sendOrderBy())
        self.tagListbox.delete(0, END)
        for row in self.tagQuery:
            self.tagListbox.insert(END, row[1])
        return



    def addTag(self):
        tag_db.addIfNotExist(self.tagNameEdit.get())
        self.searchTagByName()

    def removeTag(self):
        fato_db.removeTagFato(tag_db.findTagId(self.tagNameEdit.get()))
        tag_db.delete(tag_db.findTagId(self.tagNameEdit.get()))
        self.search_command()
        self.searchTagByName()

    def _buildPlayerSpace(self):


        global imgPlay, stop_img, prev_img, next_img, imgPause, imgSpeaker, imgMute, shuffle_img, repeat_img

        imgPlay = PhotoImage(file='icones_player/play.png')
        imgPause = PhotoImage(file='icones_player/pause.png')
        prev_img = PhotoImage(file='icones_player/prev.png')
        stop_img = PhotoImage(file='icones_player/stop.png')
        next_img = PhotoImage(file='icones_player/next.png')
        imgSpeaker = PhotoImage(file='icones_player/vol.png')
        imgMute = PhotoImage(file='icones_player/mute.png')
        repeat_img = PhotoImage(file='icones_player/repeat.png')
        # shuffle_img = PhotoImage(file='icones_player/shuffle.png')

        self.botaoPlay = Button(self.window, image=imgPlay,bd=0, command=self.playTrack)#,command=self.tocarMusica)
        self.botaoPlay.place(x=indexs.xTree,y=indexs.yPlayerGrid)

        prev_button = Button(self.window, image=prev_img,bd=0, command=self.prevTrack)#,command=lambda:self.voltarFaixa(1))
        prev_button.place(x=indexs.xTree + indexs.xPlayerGrid,y=indexs.yPlayerGrid)

        pause_button = Button(self.window, image=imgPause, command=self.pauseTrack)
        pause_button.place(x=indexs.xTree + (indexs.xPlayerGrid * 2), y=indexs.yPlayerGrid)

        next_button = Button(self.window, image=next_img,bd=0, command=self.nextTrack)#,command=lambda:self.voltarFaixa(2))
        next_button.place(x=indexs.xTree + (indexs.xPlayerGrid * 3),y=indexs.yPlayerGrid)

        stop_button = Button(self.window, image=stop_img, command=self.stopTrack)
        stop_button.place(x=indexs.xTree + (indexs.xPlayerGrid * 4), y=indexs.yPlayerGrid)


        repeat_button = Button(self.window, image=repeat_img,bd=0, command=self.loopTrack)
        repeat_button.place(x=indexs.xTree + (indexs.xPlayerGrid * 5),y=indexs.yPlayerGrid)

        self.rateMode = ttk.Spinbox(self.window, values=indexs.lstRateMode, width=4, command=self.rateTrack)
        self.rateMode.place(x=indexs.xTree + (indexs.xPlayerGrid * 6), y=indexs.yPlayerGrid)
        self.rateMode.set(1)

        speaker = Button(self.window, image=imgSpeaker, bd=0, command=self.muteTrack)
        speaker.place(x=indexs.xTree + (indexs.xPlayerGrid * 7), y=indexs.yPlayerGrid)

        play_des = Label(self.window, text='Play/Pause',relief='groove')
        prev_des = Label(self.window, text='Previous Track',relief='groove')
        stop_des = Label(self.window, text='Stop Music',relief='groove')
        next_des = Label(self.window, text='Next Track',relief='groove')
        shuffle_des = Label(self.window, text='Shuffle All',relief='groove')
        repetirTodos_des = Label(self.window, text='Repeat All',relief='groove')
        vol_des = Label(self.window, text='Adjust Volume',relief='groove')


        ## Volume Scale - adjust volume
        self.scaleVolume = ttk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)#,command=self.set_vol)
        self.scaleVolume.set(100)  # implement the default value of scale when music MusicPlayer.py starts
        self.scaleVolume.place(x=indexs.xTree + (indexs.xPlayerGrid * 8), y=indexs.yPlayerGrid)
        self.scaleVolume.bind('<ButtonRelease-1>', self._adjustVolume)


        ## Time Durations
        self.tempoComeco = Label(self.window, text='--:--',font=('Calibri',10,'bold'))
        self.tempoComeco.place(x= indexs.xTree, y=indexs.yPlayerGrid - 25)
        self.tempoFinal = Label(self.window, text='--:--',font=('Calibri',10,'bold'))
        self.tempoFinal.place(x= indexs.xTree +  970, y=indexs.yPlayerGrid - 25)

        ## Progress Bar - The progress bar which indicates the running music
        self.tempoBarra = ttk.Progressbar(self.window, orient='horizontal',length=250)
        self.tempoBarra['value'] = 0
        #self.tempoBarra.place(x=42 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)
        self.scaleTime = ttk.Scale(self.window, from_=0, to=100, length=935, orient=HORIZONTAL)
        self.scaleTime.place(x= indexs.xTree + 40, y=indexs.yPlayerGrid - 25)
        self.scaleTime.bind('<ButtonRelease-1>', self._adjustPosSample)

    def _adjustPosSample(self, event):
        self.samplePlayer.setPosition(self.scaleTime.get()/100)

    def _adjustVolume(self, event):
        self.samplePlayer.setVolume(int(self.scaleVolume.get()))


    def audioMetaData(self):
        audio = audio_metadata.load(self.treeRowValue[indexs.selectedTreePath] + '/' + self.treeRowValue[indexs.selectedTreeSample])
        self.timeSample = int(audio.streaminfo.duration + 0.5)
        self.tempoBarra["value"] = 0
        self.tempoBarra["maximum"] = 100
        self.fillTimeInfo()

    def fillTimeInfo(self):
        self.tempoFinal['text'] = self.convert(self.timeSample)
        self.tempoComeco['text'] = '00:00'


    def playTrack(self):
        self.samplePlayer.playSample()
        self.isPausedStatus = False
        self.resetTime()
        self.startTime()

    def pauseTrack(self):
        if self.treeRowValue != []:
            self.samplePlayer.pauseSample()
            self.isPausedStatus = not self.isPausedStatus


    def stopTrack(self):
        if self.treeRowValue != []:
            self.samplePlayer.stopSample()
            self.resetTime()
            self.loopMode = False
            self.isPausedStatus = False
            self.scaleTime.set(0)
            self.tempoComeco['text'] = '00:00'

    def nextTrack(self):
        if self.treeRowValue != []:
            self.tree.event_generate('<Down>')
            self.samplePlayer.pauseSample()
            self.changeSelectedSample()
            self.samplePlayer.playSample()

    def prevTrack(self):
        if self.treeRowValue != []:
            self.tree.event_generate('<Up>')
            self.samplePlayer.pauseSample()
            self.changeSelectedSample()
            self.samplePlayer.playSample()

    def muteTrack(self):
        if self.scaleVolume.get() > 5:
            self.scaleVolume.set(0)
            self.samplePlayer.setVolume(0)
        else:
            self.scaleVolume.set(70)
            self.samplePlayer.setVolume(70)

    def loopTrack(self):
        self.loopMode = not self.loopMode

    def rateTrack(self):
        if self.treeRowValue != []:
            print(self.rateMode.get())
            self.samplePlayer.setRate(float(self.rateMode.get()))
            #self.samplePlayer.setRate(1.5)

    def update_clock(self):

        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.window.after(1000, self.update_clock)
        #print(self.samplePlayer.isPlaying())
        if self.selectedSample != None:
            if self.samplePlayer.isPlaying() == 0 and self.isPausedStatus == False and self.loopMode == True:
                print('Deveria tocar')
                self.playTrack()

    def resetTime(self):
        self.countTime = 1
        self.totalTime = 0

    def startTime(self):
        self.countTime = 0
        self.timer()

    def stopTime(self):
        self.countTime = 1


    def timer(self):
        if (self.countTime == 0):
            #print(self.totalTime)
            self.tempoBarra["value"] = int(self.samplePlayer.getPosition()*100)
            self.scaleTime.set(int(self.samplePlayer.getPosition() * 100))
            if (self.countTime == 0):
                self.window.after(1000, self.timer)
                self.totalTime = self.totalTime + 1
                self.tempoComeco['text'] = self.convert(int(self.samplePlayer.getTime()/1000))

    def convert(self, seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return "%d:%02d:%02d" % (hour, min, sec) if hour != 0 else "%02d:%02d" % (min, sec)

    def autoTag(self):
        lstAutoTag = smartTag.autoTag()
        for i in lstAutoTag:
            fato_db.addIfNotExist(i[1], i[2])
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.search_command()


    def syncTag(self):
        syncRowFact = self.factQuery[self.indexSample]
        syncRowTag = self.tagQuery[self.indexTag]

        print(syncRowFact)
        print(syncRowTag)
        print(syncRowFact[1])
        print(syncRowTag[0])
        fato_db.updateTag(syncRowFact[0], syncRowTag[0])
        #self.refresh()
        self.search_command()

    def untag(self):
        syncRowFact = self.factQuery[self.indexSample]
        syncRowTag = self.tagQuery[self.indexTag]

        print(syncRowFact)
        print(syncRowTag)
        print(syncRowFact[1])
        print(syncRowTag[0])
        fato_db.removeTagFatoRow(syncRowFact[indexs.fatoQueryIdFato], syncRowFact[indexs.fatoQueryIdTag])
        #self.refresh()
        self.search_command()

    def view_command(self):
        #self.modeTagQuery['text'] = 'View All'
        self.tagListbox.delete(0, END)
        self.tagQuery = tag_db.viewall()
        self.displayTags = []
        for row in self.tagQuery:
            self.displayTags.append(row[1])
            self.tagListbox.insert(END, row[1])

    def search_command(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = fato_db.selectFilter(name=self.sampleSearch.get(), path=self.pathSearch.get(), extension=self.extensionSearch.get(),
                                     disk=self.diskSearch.get(), tag = self.tagSearch.get(), bpm = self.bpmSearch.get(), key = self.keySearch.get(), genre = self.genreSearch.get(), loveLow=self.loveLowSearch.get(), loveUpper=self.loveUpperSearch.get())
        self.new_data(query)

    def new_data(self, query):
        self.indexSample = 0
        self.factQuery = query
        cont = 1
        for item in self.factQuery:
            self.insertTreeData(cont, [item[2], item[7], item[3], item[4], item[5], item[8], item[9], item[10], item[11]])
            cont  = cont + 1

        #tree.insert('', 'end', text = 'your text', tags = ('oddrow',))
        #tree.tag_configure('oddrow', background='orange')


    def delete_command(self):
        fato_db.delete(self.treeRowValue[0])
        # sample_db.delete(self.treeRowValue[1])
        self.view_command()

    ## Add musicas to the playlist.
    def abreFaixasDir(self):
        dir_ = filedialog.askdirectory(initialdir='D:\\', title='Select Directory')
        listDir.runCode(dir_)

    def abrirMusica(self):
        dir_ = filedialog.askopenfilename(initialdir='D:/', title='Select File')
        filename = dir_.split('/')[-1]
        cng_dir = dir_.split('/')[0:-1]
        cng_dir = '/'.join(cng_dir)
        cng_dir = cng_dir + '/'
        # os.chdir(cng_dir)
        # filename = os.path.basename(dir_)
        print(dir_, cng_dir, '----', filename, filename[-3:])
        #sample_db.add(filename, cng_dir, filename[-3:], 'mac', cdate)


class SampleInfo2:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        Pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.window)
        self.app = SampleInfo2(self.newWindow)


    def close_windows(self):
        self.master.destroy()

def main():
    samplePage()

if __name__ == '__main__':
    main()

