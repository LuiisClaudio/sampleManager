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

global count

class samplePage:

    def __init__(self):

        # global self.window
        global nameLabel, pathLabel, extensionLabel, diskLabel
        global lb, sb
        global tagSearchEntry, tagSearchType, sbTagListBox, tagSearchStr
        global e1, e2, e3, e4
        global b1, b2, b3, b4, b5, b6
        global name, pathEntry, extensionEntry, extensionEntry, diskEntry, cdate, directory
        global nameAndOr, pathAndOr, extensionAndOr, diskAndOr, lstAndOr

        self.window = Tk()
        self.window.title("Manage Sample")
        self.window.geometry("1000x1000")
        #self.window.resizable(0, 0)

        self.samplePlayer = MusicPlayer.Teste()

        self.treeRowValue = []

        ManagaeTagButton = Button(self.window, text='Manage tag.', bd=2, font=('arialblack', 13), width=10, command=self.new_window)#.grid(row=7, column=2, columnspan=4)

        directory = 'D:\\'

        self.factQuery = []
        self.tagQuery = []

        self.t = StringVar()
        self.t.set("00:00:00")

        nameLabel = Label(self.window, text="Name")

        pathLabel = Label(self.window, text="Path")

        extensionLabel = Label(self.window, text="Extension")

        diskLabel = Label(self.window, text="Disk")

        name = StringVar()
        e1 = Entry(self.window, textvariable=name, width=50)

        pathEntry = StringVar()
        e2 = Entry(self.window, textvariable=pathEntry, width=50)

        extensionEntry = StringVar()
        e3 = Entry(self.window, textvariable=extensionEntry, width=50)

        diskEntry = StringVar()
        e4 = Entry(self.window, textvariable=diskEntry, width=50)


        cdate = date.today().strftime("%d/%m/%Y")


        syncTagButton = Button(self.window, text="Sync Tag", width=12, command=self.syncTag)

        AddFolderButton = Button(self.window, text='Add a Folder.', bd=2, font=('arialblack', 13), width=15, command=self.abreFaixasDir)

        AutoTagButton = Button(self.window, text='Autotag', bd=2, font=('arialblack', 13), width=10, command=self.autoTag)

        SearchTagButton = Button(self.window, text='Search Tag', bd=2, font=('arialblack', 13), width=10, command=self.searchTag)

        lb = Listbox(self.window, height=5, width=94)

        sb = Scrollbar(self.window)

        lb.configure(yscrollcommand=sb.set)
        sb.configure(command=lb.yview)

        lb.bind('<<ListboxSelect>>', self.getSelectedRow)

        tagSearchStr = StringVar()
        tagSearchEntry = Entry(self.window, textvariable=tagSearchStr, width=15)#.grid(row=2, column=6)

        tagSearchType = IntVar()
        Checkbutton(self.window, text="Last or Recent", width=12, variable=tagSearchType, command=self.showTags)#.grid(row=3, column=6)




        self._buildSampleSpace()

        self._buildTagSpace()

        self._buildPlayerSpace()

        self.showTags()

        self.window.mainloop()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.window)
        self.app = TagPage(self.newWindow)

    def _buildSampleSpace(self):

        global editSampleKey

        self._create_treeview()

        Button(self.window, text='Search', bd=2, font=('arialblack', 13), width=5, command=self.search_command).place(x = 10, y = 10)
        Button(self.window, text='Save', bd=2, font=('arialblack', 13), width=5, command=self.editSampleInfo).place(x = 400, y = 550)

        self.sampleSearch = StringVar()
        #self.sampleSearch.set("Name")
        Entry(self.window, textvariable=self.sampleSearch, width=10).place(x = 10, y = 40)

        self.pathSearch = StringVar()
        #self.pathSearch.set("Name")
        Entry(self.window, textvariable=self.pathSearch, width=10).place(x=10, y=70)

        self.extensionSearch = StringVar()
        #self.extensionSearch.set("Name")
        Entry(self.window, textvariable=self.extensionSearch, width=10).place(x=10, y=100)

        self.diskSearch = StringVar()
        #self.diskSearch.set("Name")
        Entry(self.window, textvariable=self.diskSearch, width=10).place(x=10, y=130)

        self.bpmSearch = ttk.Spinbox(self.window, values=indexs.lstBpm, width=3)
        self.bpmSearch.place(x = 120, y = 40)

        self.keySearch = ttk.Combobox(self.window, values=indexs.lstKey, width=5)
        self.keySearch.place(x = 180, y = 40)

        self.genreSearch = ttk.Combobox(self.window, values=indexs.lstGenre, width=10)
        self.genreSearch.place(x = 260, y = 40)

        self.tagSearch = StringVar()
        #tagSearch.set("Tag")
        Entry(self.window, textvariable=self.tagSearch, width=10).place(x = 380, y = 40)

        self.loveLowSearch = ttk.Spinbox(self.window, values=indexs.lstLove, width=3)
        self.loveLowSearch.place(x=490, y=40)
        self.loveUpperSearch =ttk.Spinbox(self.window, values=indexs.lstLove, width=3)
        self.loveUpperSearch.place(x=550, y=40)

        Label(self.window, text="Name").place(x=10, y=550)
        Label(self.window, text="Tag").place(x=10, y=600)  # .place(x=10, y=750)
        Label(self.window, text="BPM").place(x=10, y=650)#.place(x=10, y=600)
        Label(self.window, text="Key").place(x=10, y=700)#.place(x=10, y=650)
        Label(self.window, text="Genre").place(x=10, y=750)#.place(x=10, y=700)
        Label(self.window, text="Love").place(x=10, y=800)


        self.editSampleName =  Label(self.window, text="Name")
        self.editSampleName.place(x=100, y=550)

        self.tagListComboBox = []
        for i in tag_db.viewallNames():
            self.tagListComboBox.append(i[0])
        self.editSampleTag = ttk.Combobox(self.window, values=self.tagListComboBox)
        self.editSampleTag.place(x=100, y=600)#.place(x=100, y=750)

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
        self.tree = ttk.Treeview(self.window, columns=self.dataCols, show='headings', height = 20)
        self.tree.place(x = 10, y = 150)
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

        self._load_data()


    def _load_data(self):
        # add data to the tree
        self.indexSample = 0
        self.factQuery = fato_db.selectAll()
        cont = 1
        for item in self.factQuery:
            self.tree.insert('', 'end', values=[cont, item[2], item[7], item[3], item[4], item[5], item[8], item[9], item[10], item[11]])
            cont  = cont + 1
        #for i in self.dataCols:
        #    self.tree.column(i, width=75, minwidth=100)
        self.tree.column('Index', width=35, minwidth=35)
        self.tree.column('Sample', width=100, minwidth=150)
        self.tree.column('Tag', width=100, minwidth=100)
        self.tree.column('Path', width=100, minwidth=200)
        self.tree.column('Extension', width=30, minwidth=30)
        self.tree.column('Disk', width=30, minwidth=30)
        self.tree.column('BPM', width=35, minwidth=35)
        self.tree.column('Key', width=35, minwidth=35)
        self.tree.column('Genre', width=100, minwidth=100)
        self.tree.column('Love', width=35, minwidth=35)

        #tree.insert('', 'end', text = 'your text', tags = ('oddrow',))
        #tree.tag_configure('oddrow', background='orange')

    def selectTreeValues(self, event):
        curItem = self.tree.focus()
        treeValue = self.tree.item(curItem)
        self.treeRowValue = treeValue['values']
        print('-->',self.treeRowValue)
        self.indexSample = self.treeRowValue[0] - 1
        self.samplePlayer.changeSample(self.treeRowValue[1], self.treeRowValue[3], self.treeRowValue[4])
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
        self.samplePlayer.changeSample(self.treeRowValue[1], self.treeRowValue[3], self.treeRowValue[4])
        self.fillSampleInfo()
        self.audioMetaData()

    def fillSampleInfo(self):
        def searchIndexTag(name):
            found = False
            for position in (x for x, n in enumerate(self.tagListComboBox) if n == name):
                self.tagListComboBox[position]
                return position
            if not found:
                return 0

        self.editSampleName['text'] = self.treeRowValue[indexs.selectedTreeSample]

        #self.editSampleKey.current(indexs.lstKey.index(self.treeRowValue[indexs.selectedTreeKey]))

        self.editSampleTag.current(searchIndexTag(self.treeRowValue[indexs.selectedTreeTag]))
        self.editSampleBpm.set(self.treeRowValue[indexs.selectedTreeBpm])
        self.editSampleKey.current(indexs.lstKey.index(self.treeRowValue[indexs.selectedTreeKey]))
        self.editSampleGenre.current(indexs.lstGenre.index(self.treeRowValue[indexs.selectedTreeGenre]))

        self.editSampleLove.set(self.treeRowValue[indexs.selectedTreeLove])

    def editSampleInfo(self):
        def searchIdTag(name):
            return tag_db.findTagId(name)

        print(self.factQuery[self.treeRowValue[indexs.selectedTreeCount] - 1])
        id_fato = self.factQuery[self.treeRowValue[indexs.selectedTreeCount] - 1][indexs.fatoQueryIdFato]
        love = self.editSampleLove.get()
        id_tag = searchIdTag(self.editSampleTag.get())
        id_sample = self.factQuery[self.treeRowValue[indexs.selectedTreeCount] - 1][indexs.fatoQueryIdSample]
        print(id_fato, love, id_tag)
        fato_db.updateByInterface(id_fato, id_sample, love, id_tag)


        bpm = self.editSampleBpm.get()
        key = self.editSampleKey.get()
        genre = self.editSampleGenre.get()
        print(id_sample, bpm, key, genre)
        sample_db.updateByInterface(id_sample, bpm, key, genre)

        self.refresh()

    def _buildTagSpace(self):
        value = StringVar()
        self.modeTagQuery = ttk.Combobox(self.window, values=['Name', 'Most Used', 'Last Used'], width = 10, state='readonly')
        self.modeTagQuery.place(x = indexs.xTagGrid, y = 150 - 20)
        self.modeTagQuery.current(0)
        self._createListTag()

        Button(self.window, text='Add', bd=2, font=('arialblack', 13), width=5, command=self.addTag).place(x=indexs.xTagGrid, y=10)
        Button(self.window, text='Remove', bd=2, font=('arialblack', 13), width=5, command=self.removeTag).place(x=indexs.xTagGrid + 60, y=10)
        #Button(self.window, text='Edit', bd=2, font=('arialblack', 13), width=5, command='').place(x=indexs.xTagGrid + 120, y=10)

        self.tagNameEdit = StringVar()
        self.tagNameEditEntry = Entry(self.window, textvariable=self.tagNameEdit, width=10)
        self.tagNameEditEntry.place(x=indexs.xTagGrid, y=40)
        Button(self.window, text='Search', bd=2, font=('arialblack', 13), width=5, command=self.searchTagByName).place(x=indexs.xTagGrid, y=100)

        self.tagSearchNameEntry = StringVar()
        #self.tagSearch.set("Name")
        Entry(self.window, textvariable=self.tagSearchNameEntry, width=10).place(x=indexs.xTagGrid + 50, y=100)

        Button(self.window, text="Sync Tag", width=12, command=self.syncTag).place(x=indexs.xTagGrid  - 130, y=200)

    def _createListTag(self):
        self.tagListbox = Listbox(self.window, height=15, width=20)
        self.tagListbox.place(x = indexs.xTagGrid, y = 150)
        self.indexTag = 0

        sb = Scrollbar(self.window)
        #sb.grid(row=1, column=2, rowspan=6)

        self.tagListbox.configure(yscrollcommand=sb.set)
        sb.configure(command=self.tagListbox.yview)

        self.tagListbox.bind('<<ListboxSelect>>', self.getSelectedRow)
        self.view_command()

    def getSelectedRow(self, event):
        try:
            global selectedTuple
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

    def showTags(self):
        if tagSearchType.get() == 0:
            # self.modeTagQuery['text'] = "View Most Used"
            self.tagQuery = tag_db.viewMostUsed()
            self.tagListbox.delete(0, END)
            for row in self.tagQuery:
                self.tagListbox.insert(END, row[1])

    def addTag(self):
        tag_db.addIfNotExist(self.tagSearchNameEntry.get())
        self.refresh()

    def removeTag(self):
        tag_db.delete(tag_db.findTagId(self.tagSearchNameEntry.get()))
        self.refresh()

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
        self.botaoPlay.place(x=10 + indexs.xPlayerGrid,y=440 + indexs.yPlayerGrid)

        prev_button = Button(self.window, image=prev_img,bd=0, command=self.prevTrack)#,command=lambda:self.voltarFaixa(1))
        prev_button.place(x=50 + indexs.xPlayerGrid,y=433 + indexs.yPlayerGrid)

        stop_button = Button(self.window, image=stop_img, command=self.stopTrack)
        stop_button.place(x=85 + indexs.xPlayerGrid,y=438 + indexs.yPlayerGrid)

        next_button = Button(self.window, image=next_img,bd=0, command=self.nextTrack)#,command=lambda:self.voltarFaixa(2))
        next_button.place(x=113 + indexs.xPlayerGrid,y=433 + indexs.yPlayerGrid)

        speaker = Button(self.window,image=imgSpeaker,bd=0)#,command=self.speaker_func)
        speaker.place(x=50 + indexs.xPlayerGrid,y=500 + indexs.yPlayerGrid)

        #shuffle_button = Button(self.window, image=shuffle_img,bd=0)#,command=lambda:self.modoRepeticao(1))
        #shuffle_button.place(x=170 + indexs.xPlayerGrid,y=440 + indexs.yPlayerGrid)

        repeat_button = Button(self.window, image=repeat_img,bd=0)#,command=lambda:self.modoRepeticao(2))
        repeat_button.place(x=200 + indexs.xPlayerGrid,y=440 + indexs.yPlayerGrid)


        play_des = Label(self.window, text='Play/Pause',relief='groove')
        prev_des = Label(self.window, text='Previous Track',relief='groove')
        stop_des = Label(self.window, text='Stop Music',relief='groove')
        next_des = Label(self.window, text='Next Track',relief='groove')
        shuffle_des = Label(self.window, text='Shuffle All',relief='groove')
        repetirTodos_des = Label(self.window, text='Repeat All',relief='groove')
        vol_des = Label(self.window, text='Adjust Volume',relief='groove')


        ## Volume Scale - adjust volume
        scale = ttk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)#,command=self.set_vol)
        scale.set(70)  # implement the default value of scale when music MusicPlayer.py starts
        scale.place(x=100 + indexs.xPlayerGrid,y=500 + indexs.yPlayerGrid)


        ## Time Durations
        self.tempoComeco = Label(self.window, text='--:--',font=('Calibri',10,'bold'))
        self.tempoComeco.place(x=5 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)
        self.tempoFinal = Label(self.window, text='--:--',font=('Calibri',10,'bold'))
        self.tempoFinal.place(x=300 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)

        ## Progress Bar - The progress bar which indicates the running music
        tempoBarra = ttk.Progressbar(self.window, orient='horizontal',length=200)
        tempoBarra.place(x=42 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)



    def audioMetaData(self):
        audio = audio_metadata.load(self.treeRowValue[indexs.selectedTreePath] + '/' + self.treeRowValue[indexs.selectedTreeSample])
        print('----', audio.streaminfo.duration)
        self.timeSample = audio.streaminfo.duration
        self.tempoFinal['text'] = self.timeSample
        self.tempoComeco['text'] = '0'


    def playTrack(self):
        if self.treeRowValue != []:
            self.samplePlayer.playSample()
            self.reset()
            self.start()

    def stopTrack(self):
        if self.treeRowValue != []:
            self.samplePlayer.stopSample()
            self.stop()
            self.reset()

    def nextTrack(self):
        if self.treeRowValue != []:
            self.tree.event_generate('<Down>')
            self.samplePlayer.pauseSample()
            self.samplePlayer.changeSample(self.treeRowValue[1], self.treeRowValue[3], self.treeRowValue[4])
            self.samplePlayer.playSample()

    def prevTrack(self):
        if self.treeRowValue != []:
            self.tree.event_generate('<Up>')
            self.samplePlayer.pauseSample()
            self.samplePlayer.changeSample(self.treeRowValue[1], self.treeRowValue[3], self.treeRowValue[4])
            self.samplePlayer.playSample()

    def reset(self):
        global count
        count = 1
        self.t.set('00:00')

    def start(self):
        global count
        count = 0
        self.start_timer()

    def start_timer(self):
        global count
        self.timer()

    def stop(self):
        global count
        count = 1

    def timer(self):
        global count
        if (count == 0):
            self.d = str(self.t.get())
            m, s = map(int, self.d.split(":"))

            m = int(m)
            s = int(s)
            if (s < 59):
                s += 1
            elif (s == 59):
                s = 0
                if (m < 59):
                    m += 1
            if (m < 10):
                m = str(0) + str(m)
            else:
                m = str(m)
            if (s < 10):
                s = str(0) + str(s)
            else:
                s = str(s)
            self.d = m + ":" + s
            print(self.d)

            self.t.set(self.d)
            self.tempoComeco['text'] = self.d
            if (count == 0):
                self.window.after(930, self.start_timer)


    def autoTag(self):
        lstAutoTag = smartTag.autoTag()
        for i in lstAutoTag:
            fato_db.addIfNotExist(i[1], i[2])
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self._load_data()
        self.showTags()

    def syncTag(self):
        syncRowFact = self.factQuery[self.indexSample]
        syncRowTag = self.tagQuery[self.indexTag]

        print(syncRowFact)
        print(syncRowTag)
        print(syncRowFact[1])
        print(syncRowTag[0])
        fato_db.updateTag(syncRowFact[0], syncRowTag[0])
        self.refresh()

    def syncNewTag(self):
        syncRowFact = self.factQuery[self.indexSample]
        syncRowTag = self.tagQuery[self.indexTag]
        fato_db.addTag(syncRowFact[1], syncRowTag[0])
        self.refresh()


    def searchTag(self):
        print(tagSearchStr.get())
        self.tagQuery = tag_db.search(tagSearchStr.get())
        self.tagListbox.delete(0, END)
        for row in self.tagQuery:
            self.tagListbox.insert(END, row[1])

    def view_command(self):
        #self.modeTagQuery['text'] = 'View All'
        self.tagListbox.delete(0, END)
        self.tagQuery = tag_db.viewall()
        self.displayTags = []
        for row in self.tagQuery:
            self.displayTags.append(row[1])
            self.tagListbox.insert(END, row[1])

    def search_command(self):
        lb.delete(0, END)
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = fato_db.selectFilter(name=self.sampleSearch.get(), path=pathEntry.get(), extension=extensionEntry.get(),
                                     disk=diskEntry.get(), tag = self.tagSearch.get(), bpm = self.bpmSearch.get(), key = self.keySearch.get(), genre = self.genreSearch.get(), loveLow=self.loveLowSearch.get(), loveUpper=self.loveUpperSearch.get())
        self.new_data(query)

    def new_data(self, query):
        self.indexSample = 0
        self.factQuery = query
        cont = 1
        for item in self.factQuery:
            self.tree.insert('', 'end', values=[cont, item[2], item[7], item[3], item[4], item[5], item[8], item[9], item[10], item[11]])
            cont  = cont + 1

        #tree.insert('', 'end', text = 'your text', tags = ('oddrow',))
        #tree.tag_configure('oddrow', background='orange')

    def add_command(self):
        tag_db.add(name.get(), cdate.get())
        sample_db.add(name.get(), pathEntry.get(), extensionEntry.get(), diskEntry.get(), cdate.get())
        lb.delete(0, END)
        lb.insert(END, name.get(), cdate.get())

    def update_command(self):
        sample_db.update(self.treeRowValue[1], name=name.get(), path=pathEntry.get(), extension=extensionEntry.get(),
                         disk=diskEntry.get(), date=cdate)
        self.view_command()
        self.refresh()

    def delete_command(self):
        fato_db.delete(self.treeRowValue[0])
        # sample_db.delete(self.treeRowValue[1])
        self.view_command()

    def clear_command(self):
        lb.delete(0, END)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

    ## Add musicas to the playlist.
    def abreFaixasDir(self):
        music_ex = ['mp3', 'ogg']
        dir_ = filedialog.askdirectory(initialdir='D:\\', title='Select Directory')
        directory = dir_
        listDir.runCode(dir_)
        # os.chdir(dir_)
        # dir_files = os.listdir(dir_)
        # for file in dir_files:
        #     exten = file.split('.')[-1]
        #     for ex in music_ex:
        #         if exten == ex:
        #             print(file)

    def abrirMusica(self):
        dir_ = filedialog.askopenfilename(initialdir='D:/', title='Select File')
        filename = dir_.split('/')[-1]
        cng_dir = dir_.split('/')[0:-1]
        cng_dir = '/'.join(cng_dir)
        cng_dir = cng_dir + '/'
        # os.chdir(cng_dir)
        # filename = os.path.basename(dir_)
        print(dir_, cng_dir, '----', filename, filename[-3:])
        sample_db.add(filename, cng_dir, filename[-3:], 'mac', cdate)


class TagPage:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        # self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        # self.quitButton.pack()

        # top = Toplevel()
        # top.title("Anexo")
        # Label(top, text="Name").grid(row=0, column=0, columnspan=2)

        global lbTag, nameTagEntry, nameTag, cdate

        cdate = date.today().strftime("%d/%m/%Y")

        nameLabel = Label(self.frame, text="Name")
        nameLabel.grid(row=0, column=0, columnspan=2)

        lbTag = Listbox(self.frame, height=20, width=94)
        lbTag.grid(row=6, column=0, columnspan=6)

        sbTag = Scrollbar(self.frame)
        sbTag.grid(row=6, column=6, rowspan=6)

        lbTag.configure(yscrollcommand=sbTag.set)
        sbTag.configure(command=lbTag.yview)

        lbTag.bind('<<ListboxSelect>>', self.getSelectedRowTag)

        nameTag = StringVar()
        nameTagEntry = Entry(self.frame, textvariable=nameTag, width=50).grid(row=0, column=0, columnspan=10)

        bTag1 = Button(self.frame, text="Add", width=12, command=self.add_commandTag)
        bTag1.grid(row=5, column=0)

        bTag2 = Button(self.frame, text="Update", width=12, command=self.update_commandTag)
        bTag2.grid(row=5, column=1)

        bTag3 = Button(self.frame, text="Search", width=12, command='')
        bTag3.grid(row=5, column=2)

        bTag4 = Button(self.frame, text="View All", width=12, command=self.view_commandTag)
        bTag4.grid(row=5, column=3)

        bTag5 = Button(self.frame, text="Delete", width=12, command=self.delete_commandTag)
        bTag5.grid(row=5, column=4)

        bTag6 = Button(self.frame, text="Cancel", width=12, command=self.frame.destroy)
        bTag6.grid(row=5, column=5)

        bTag7 = Button(self.frame, text="Clear All", width=12, command=self.clear_commandTag)
        bTag7.grid(row=0, column=5)

        self.frame.pack()
        Pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.window)
        self.app = TagPage(self.newWindow)

    def getSelectedRowTag(self, event):
        try:
            global selectedTupleTag
            index = lbTag.curselection()[0]
            selectedTupleTag = lbTag.get(index)
            # nameTagEntry.delete(0,END)
            nameTagEntry.insert(END, selectedTupleTag[1])
        except IndexError:
            pass

    def view_commandTag(self):
        lbTag.delete(0, END)
        for row in tag_db.viewall():
            lbTag.insert(END, row)


    def add_commandTag(self):
        tag_db.add(nameTag.get(), cdate)
        lbTag.delete(0, END)
        lbTag.insert(END, nameTag.get(), cdate)

    def update_commandTag(self):
        tag_db.update(selectedTupleTag[0], nameTag.get(), cdate)
        self.view_command()

    def delete_commandTag(self):
        tag_db.delete(selectedTupleTag[0])
        self.view_command()

    def clear_commandTag(self):
        lbTag.delete(0, END)
        nameTagEntry.delete(0, END)

    def close_windows(self):
        self.master.destroy()


def main():
    samplePage()


if __name__ == '__main__':
    main()

# interface = samplePage()
