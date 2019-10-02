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

        b1 = Button(self.window, text="Add", width=12, command=self.abrirMusica)

        b2 = Button(self.window, text="Update", width=12, command=self.update_command)

        b3 = Button(self.window, text="Search", width=12, command=self.search_command)

        b4 = Button(self.window, text="View All", width=12, command=self.view_command)

        b5 = Button(self.window, text="Delete", width=12, command=self.delete_command)

        b6 = Button(self.window, text="Cancel", width=12, command=self.window.destroy)

        b7 = Button(self.window, text="Clear All", width=12, command=self.clear_command)

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

        self._create_treeview()

        Button(self.window, text='Search', bd=2, font=('arialblack', 13), width=5, command='').place(x = 10, y = 10)
        Button(self.window, text='Like', bd=2, font=('arialblack', 13), width=5, command='').place(x = 100, y = 10)

        sampleSearch = StringVar()
        sampleSearch.set("Name")
        Entry(self.window, textvariable=sampleSearch, width=10).place(x = 10, y = 40)

        ttk.Spinbox(self.window, values=indexs.lstBpm, width=3).place(x = 120, y = 40)

        ttk.Combobox(self.window, values=indexs.lstKey, width=5).place(x = 180, y = 40)

        ttk.Combobox(self.window, values=indexs.lstGenre, width=10).place(x = 260, y = 40)

        tagSearch = StringVar()
        tagSearch.set("Tag")
        Entry(self.window, textvariable=tagSearch, width=10).place(x = 380, y = 40)

        ttk.Spinbox(self.window, values=indexs.lstLove, width=3).place(x=490, y=40)
        ttk.Spinbox(self.window, values=indexs.lstLove, width=3).place(x=550, y=40)

        Label(self.window, text="Name").place(x=10, y=550)
        Label(self.window, text="BPM").place(x=10, y=600)
        Label(self.window, text="Key").place(x=10, y=650)
        Label(self.window, text="Genre").place(x=10, y=700)
        Label(self.window, text="Tag").place(x=10, y=750)
        Label(self.window, text="Love").place(x=10, y=800)


        Label(self.window, text="Name").place(x=100, y=550)

        ttk.Spinbox(self.window, values=indexs.lstBpm, width=3).place(x=100, y=600)
        ttk.Combobox(self.window, values=indexs.lstKey, width=5).place(x=100, y=650)
        ttk.Combobox(self.window, values=indexs.lstGenre, width=10).place(x=100, y=700)
        ttk.Combobox(self.window, values=tag_db.viewall()).place(x=100, y=750)
        ttk.Spinbox(self.window, values=indexs.lstLove, width=10).place(x=100, y=800)


    def _create_treeview(self):
        self.dataCols = ["Index", "Sample", "Path", "Extension", "Disk", "Tag"]  # ['name', 'path', 'extension']
        self.tree = ttk.Treeview(self.window, columns=self.dataCols, show='headings', height = 20)
        self.tree.place(x = 10, y = 150)
        self.tree.bind('<ButtonRelease-1>', self.selectTreeValues)

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
            self.tree.insert('', 'end', values=[cont, item[2], item[7], item[3], item[4], item[5]])
            cont  = cont + 1
        #for i in self.dataCols:
        #    self.tree.column(i, width=75, minwidth=100)
        self.tree.column('Index', width=100, minwidth=35)
        self.tree.column('Sample', width=100, minwidth=150)
        self.tree.column('Tag', width=100, minwidth=100)
        self.tree.column('Path', width=100, minwidth=200)
        self.tree.column('Extension', width=100, minwidth=40)
        self.tree.column('Disk', width=100, minwidth=40)

        #tree.insert('', 'end', text = 'your text', tags = ('oddrow',))
        #tree.tag_configure('oddrow', background='orange')

    def selectTreeValues(self, event):
        curItem = self.tree.focus()
        treeValue = self.tree.item(curItem)
        self.treeRowValue = treeValue['values']
        print(self.treeRowValue)
        print(self.treeRowValue[0] - 1)
        self.indexSample = self.treeRowValue[0] - 1
        self.fillEntryBox()
        self.samplePlayer.changeSample(self.treeRowValue[1], self.treeRowValue[3], self.treeRowValue[4])

    def _buildTagSpace(self):
        value = StringVar()
        self.modeTagQuery = ttk.Combobox(self.window, values=['Name', 'Most Used', 'Last Used'], width = 10, textvariable=value, state='readonly').place(x = indexs.xTagGrid, y = 150 - 20)
        #self.modeTagQuery.current[0]
        self._createListTag()

        Button(self.window, text='Add', bd=2, font=('arialblack', 13), width=5, command='').place(x=indexs.xTagGrid, y=10)
        Button(self.window, text='Remove', bd=2, font=('arialblack', 13), width=5, command='').place(x=indexs.xTagGrid + 60, y=10)
        Button(self.window, text='Edit', bd=2, font=('arialblack', 13), width=5, command='').place(x=indexs.xTagGrid + 120, y=10)

        self.tagNameEdit = StringVar()
        self.tagNameEditEntry = Entry(self.window, textvariable=self.tagNameEdit, width=10).place(x=indexs.xTagGrid, y=40)

        Button(self.window, text='Search', bd=2, font=('arialblack', 13), width=5, command='').place(x=indexs.xTagGrid, y=100)

        self.tagSearch = StringVar()
        self.tagSearch.set("Name")
        Entry(self.window, textvariable=self.tagSearch, width=10).place(x=indexs.xTagGrid + 50, y=100)

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

            #self.tagNameEditEntry.delete(0, END)
            #self.tagNameEditEntry.insert(END, selectedTupleTag)
        except IndexError:
            pass


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

        self.botaoPlay = Button(self.window, image=imgPlay,bd=0, command=self.samplePlayer.playSample)#,command=self.tocarMusica)
        self.botaoPlay.place(x=10 + indexs.xPlayerGrid,y=440 + indexs.yPlayerGrid)

        prev_button = Button(self.window, image=prev_img,bd=0, command=self.nextTrack)#,command=lambda:self.voltarFaixa(1))
        prev_button.place(x=50 + indexs.xPlayerGrid,y=433 + indexs.yPlayerGrid)

        stop_button = Button(self.window, image=stop_img, command=self.samplePlayer.stopSample)
        stop_button.place(x=85 + indexs.xPlayerGrid,y=438 + indexs.yPlayerGrid)

        next_button = Button(self.window, image=next_img,bd=0)#,command=lambda:self.voltarFaixa(2))
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
        tempoComeco = Label(self.window, text='--:--',font=('Calibri',10,'bold'))
        tempoComeco.place(x=5 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)
        tempoFinal = Label(self.window, text='--:--',font=('Calibri',10,'bold'))
        tempoFinal.place(x=300 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)

        ## Progress Bar - The progress bar which indicates the running music
        tempoBarra = ttk.Progressbar(self.window, orient='horizontal',length=200)
        tempoBarra.place(x=42 + indexs.xPlayerGrid,y=400 + indexs.yPlayerGrid)

    def nextTrack(self):
        print(self.treeRowValue)
        # print(self.factQuery[self.treeRowValue[0] + 1])
        # self.treeRowValue = self.factQuery[self.treeRowValue[0] + 1]
        # self.samplePlayer.changeSample(self.treeRowValue[1], self.treeRowValue[3], self.treeRowValue[4])

    def autoTag(self):
        lstAutoTag = smartTag.autoTag()
        for i in lstAutoTag:
            fato_db.addIfNotExist(i[1], i[2])
        self.refresh()


    def fillEntryBox(self):
        e1.delete(0, END)
        e1.insert(END, self.treeRowValue[2])
        e2.delete(0, END)
        e2.insert(END, self.treeRowValue[3])
        e3.delete(0, END)
        e3.insert(END, self.treeRowValue[4])
        e4.delete(0, END)
        e4.insert(END, self.treeRowValue[5])

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

    def showTags(self):
        if tagSearchType.get() == 0:
            #self.modeTagQuery['text'] = "View Most Used"
            self.tagQuery = tag_db.viewMostUsed()
            self.tagListbox.delete(0, END)
            for row in self.tagQuery:
                self.tagListbox.insert(END, row[1])
        else:
            #self.modeTagQuery['text'] = "View Last Used"
            self.tagQuery = tag_db.viewLastUsed()
            self.tagListbox.delete(0, END)
            for row in self.tagQuery:
                self.tagListbox.insert(END, row[1])

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
        for row in self.tagQuery:
            self.tagListbox.insert(END, row[1])

    def search_command(self):
        lb.delete(0, END)
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = fato_db.selectFilter(name=name.get(), path=pathEntry.get(), extension=extensionEntry.get(),
                                     disk=diskEntry.get())
        for row in query:
            lb.insert(END, row)
            self.tree.insert('', 'end', values=row)

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

        bTag3 = Button(self.frame, text="Search", width=12, command=self.search_commandTag)
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

    def search_commandTag(self):
        lbTag.delete(0, END)
        for row in tag_db.search(name=nameTag.get()):
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
