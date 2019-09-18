from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import sample_db
import tag_db
import fato_db
import listDir
import os
import smartTag
from datetime import date



class samplePage:

    def __init__(self, master):

        #global self.window
        global nameLabel, pathLabel, extensionLabel, diskLabel
        global lb, sb
        global tagSearchEntry, tagSearchType, tagListBox, sbTagListBox, tagSearchStr
        global e1, e2, e3, e4
        global b1, b2, b3, b4, b5, b6
        global name, pathEntry, extensionEntry, extensionEntry, diskEntry, cdate, directory
        global nameAndOr, pathAndOr, extensionAndOr, diskAndOr, lstAndOr

        
        self.window = Tk()
        self.window.title("SampleDatabase")

        directory = 'D:\\'
        lstAndOr = ['OR', 'OR', 'OR', 'OR']

        nameLabel = Label(self.window,text="Name")
        nameLabel.grid(row=0,column=0,columnspan=2)
        
        pathLabel = Label(self.window,text="Path")
        pathLabel.grid(row=1,column=0,columnspan=2)

        extensionLabel = Label(self.window,text="Extension")
        extensionLabel.grid(row=2,column=0,columnspan=2)

        diskLabel = Label(self.window,text="Disk")
        diskLabel.grid(row=3,column=0,columnspan=2)


        name=StringVar()
        e1 = Entry(self.window,textvariable=name,width=50)
        e1.grid(row=0,column=0,columnspan=10)

        pathEntry=StringVar()
        e2 = Entry(self.window,textvariable=pathEntry,width=50)
        e2.grid(row=1,column=0,columnspan=10)

        extensionEntry=StringVar()
        e3 = Entry(self.window,textvariable=extensionEntry,width=50)
        e3.grid(row=2,column=0,columnspan=10)

        diskEntry=StringVar()
        e4 = Entry(self.window,textvariable=diskEntry,width=50)
        e4.grid(row=3,column=0,columnspan=10)

        #cdate=StringVar()
        #e5 = Entry(self.window,textvariable=cdate,width=50)
        #e5.grid(row=4,column=0,columnspan=10)

        cdate = date.today().strftime("%d/%m/%Y")

        b1 = Button(self.window,text="Add",width=12,command=self.abrirMusica)
        b1.grid(row=5,column=0)
        #nameAndOr = IntVar()
        #Checkbutton(self.window,text="AND or OR",width=12, variable=nameAndOr, command=self.defineAndOr).grid(row=0,column=5)

        b2 = Button(self.window,text="Update",width=12,command=self.update_command)
        b2.grid(row=5,column=1)
        #pathAndOr = IntVar()
        #Checkbutton(self.window, text="AND or OR", width=12, variable=pathAndOr, command=self.defineAndOr).grid(row=1, column=5)

        b3 = Button(self.window,text="Search",width=12,command=self.search_command)
        b3.grid(row=5,column=2)
        #extensionAndOr = IntVar()
        #Checkbutton(self.window, text="AND or OR", width=12, variable=extensionAndOr, command=self.defineAndOr).grid(row=2, column=5)

        b4 = Button(self.window,text="View All",width=12,command=self.view_command)
        b4.grid(row=5,column=3)
        #diskAndOr = IntVar()
        #Checkbutton(self.window, text="AND or OR", width=12, variable=diskAndOr, command=self.defineAndOr).grid(row=3, column=5)

        b5 = Button(self.window,text="Delete",width=12,command=self.delete_command)
        b5.grid(row=5,column=4)

        b6 = Button(self.window,text="Cancel",width=12,command=self.window.destroy)
        b6.grid(row=5,column=5)
        
        b7 = Button(self.window,text="Clear All",width=12,command=self.clear_command)
        b7.grid(row=0,column=6)

        Button(self.window,text="Sync Tag",width=12,command=self.syncTag).grid(row=1,column=6)

        Button(self.window, text='Add a Folder.',bd=2,font=('arialblack',13),width=15,command=self.abreFaixasDir).grid(row=7,column=0,columnspan=4) #.place(x=10,y=20)
        Button(self.window, text='Manage tag.',bd=2,font=('arialblack',13),width=10,command=self.new_window).grid(row=7,column=2,columnspan=4)
        Button(self.window, text='Autotag', bd=2, font=('arialblack', 13), width=10, command=self.autoTag).grid(row=7, column=3, columnspan=4)
        Button(self.window, text='Search Tag',bd=2,font=('arialblack',13),width=10,command=self.searchTag).grid(row=5,column=6)

        lb=Listbox(self.window,height=5,width=94)
        lb.grid(row=6,column=0,columnspan=6)
        self.indexSample = 0

        sb=Scrollbar(self.window)
        sb.grid(row=6,column=6,rowspan=6)

        lb.configure(yscrollcommand=sb.set)
        sb.configure(command=lb.yview)

        lb.bind('<<ListboxSelect>>', self.getSelectedRow)

        tagSearchStr = StringVar()
        tagSearchEntry = Entry(self.window,textvariable=tagSearchStr,width=15).grid(row=2, column=6)

        tagSearchType = IntVar()
        Checkbutton(self.window, text="Last or Recent", width=12, variable=tagSearchType, command=self.showTags).grid(row=3, column=6)
        
        tagListBox=Listbox(self.window,height=5,width=20)
        tagListBox.grid(row=6,column=6,columnspan=6)
        self.indexTag = 0

        sbTagListBox=Scrollbar(self.window)
        sbTagListBox.grid(row=6,column=7,rowspan=6)

        tagListBox.configure(yscrollcommand=sbTagListBox.set)
        sbTagListBox.configure(command=tagListBox.yview)

        tagListBox.bind('<<ListboxSelect>>', self.getSelectedRowTag)

        Label(self.window, text="-----------------------------------------------").grid(row=8, column=0, columnspan=2)

        self._create_treeview()
        self._load_data()

        self.view_command()
        self.showTags()
        
        self.window.mainloop()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.window)
        self.app = TagPage(self.newWindow)

    def _create_treeview(self):
        self.dataCols = ["f.id_fato", "s.id_sample", "s.name", "s.path", "s.extension", "s.disk", "id_tag",  "tag"] #['name', 'path', 'extension']
        self.tree = ttk.Treeview(self.window, columns=self.dataCols, show = 'headings')
        self.tree.grid(row=9,column=0,columnspan=6)
        self.tree.bind('<ButtonRelease-1>', self.selectTreeValues)

        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        
        # add tree and scrollbars to frame
        ysb.grid(in_ = self.window, row=10,column=1,columnspan=6)
        xsb.grid(in_ = self.window, row=11,column=2,columnspan=6)

    def _load_data(self):
        # add data to the tree
        row = fato_db.selectAll()
        for item in row:
            self.tree.insert('', 'end', values=item)
            # and adjust column widths if necessary
            # for idx, val in enumerate(item):
            #     iwidth = Font().measure(val if val != None else "None")
            #     if self.tree.column(self.dataCols[idx], 'width') < iwidth:
            #         self.tree.column(self.dataCols[idx], width=iwidth)
        for i in self.dataCols:
            self.tree.column(i, width=100, minwidth=100)


    def autoTag(self):
        lstAutoTag = smartTag.autoTag()
        for i in lstAutoTag:
            fato_db.addIfNotExist(i[1], i[2])
        self.refresh()

    
    def selectTreeValues(self, event):
        curItem = self.tree.focus()
        treeValue = self.tree.item(curItem)
        self.treeRowValue = treeValue['values']
        print(self.treeRowValue)
        self.fillEntryBox()

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
        if self.treeRowValue[-2] != 'None':
            print('--------', self.treeRowValue[-2])
            fato_db.addTag(self.treeRowValue[1], selectedTupleTag[0])
        else:
            fato_db.updateTag(self.treeRowValue[0], selectedTupleTag[0])
        #for row in self.tree.get_children():
        #    self.tree.delete(row)
        #self._load_data()
        #self.showTags()
        self.refresh()

        
    def showTags(self):
        if tagSearchType.get() == 0:
            tagListBox.delete(0,END)
            for row in tag_db.viewMostUsed():
                tagListBox.insert(END,row)
        else:
            tagListBox.delete(0,END)
            for row in tag_db.viewLastUsed():
                tagListBox.insert(END,row)

    def searchTag(self):
        print(tagSearchStr.get())
        tagListBox.delete(0, END)
        for row in tag_db.search(tagSearchStr.get()):
            tagListBox.insert(END, row)

    def view_command(self):
        lb.delete(0,END)
        for row in fato_db.selectAll():
            lb.insert(END,row)
    

    def search_command(self):
        lb.delete(0,END)
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = fato_db.selectFilter(name=name.get(), path=pathEntry.get(), extension=extensionEntry.get(), disk=diskEntry.get())
        for row in query:
            lb.insert(END,row)
            self.tree.insert('', 'end', values=row)

        

    def add_command(self):
        tag_db.add(name.get(), cdate.get())
        sample_db.add(name.get(),pathEntry.get(),extensionEntry.get(),diskEntry.get(),cdate.get())
        lb.delete(0,END)
        lb.insert(END,name.get(),cdate.get())

    def getSelectedRowTag(self, event):
        try:
            global selectedTupleTag
            indexTagAnt = self.indexTag
            self.indexTag = tagListBox.curselection()[0]
            selectedTupleTag = tagListBox.get(self.indexTag)
            tagListBox.itemconfig(self.indexTag, bg='pale turquoise', fg='black')
            tagListBox.itemconfig(indexTagAnt, bg='white', fg='black')
            print(selectedTupleTag)
        except IndexError:
            pass

    def getSelectedRow(self, event):
        try:
            global selectedTuple
            indexSampleAnt = self.indexSample
            self.indexSample=lb.curselection()[0]
            selectedTuple = lb.get(self.indexSample)
            lb.itemconfig(self.indexSample, bg='pale turquoise', fg='black')
            lb.itemconfig(indexSampleAnt, bg='white', fg='black')
            e1.delete(0,END)
            e1.insert(END,selectedTuple[1])
            e2.delete(0,END)
            e2.insert(END,selectedTuple[2])
            e3.delete(0, END)
            e3.insert(END, selectedTuple[3])
            e4.delete(0, END)
            e4.insert(END, selectedTuple[4])
        except IndexError:
            pass

    def update_command(self):
        sample_db.update(self.treeRowValue[1], name=name.get(), path=pathEntry.get(), extension=extensionEntry.get(), disk=diskEntry.get(), date=cdate)
        self.view_command()
        self.refresh()

    def delete_command(self):
        fato_db.delete(self.treeRowValue[0])
        #sample_db.delete(self.treeRowValue[1])
        self.view_command()

    def clear_command(self):
        lb.delete(0,END)
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0, END)
        e4.delete(0, END)

    # def defineAndOr(self):
    #     if nameAndOr.get() == 0:
    #         lstAndOr[0] = 'OR'
    #     else:        
    #         lstAndOr[0] = 'AND'

    #     if  pathAndOr.get() == 0:
    #         lstAndOr[1] = 'OR'
    #     else:        
    #         lstAndOr[1] = 'AND'

    #     if extensionAndOr.get() == 0:
    #         lstAndOr[2] = 'OR'
    #     else:        
    #         lstAndOr[2] = 'AND'

    #     if diskAndOr.get() == 0:
    #         lstAndOr[3] = 'OR'
    #     else:        
    #         lstAndOr[3] = 'AND'


    
    ## Add musicas to the playlist.
    def abreFaixasDir(self):
        music_ex = ['mp3','ogg']
        dir_ =  filedialog.askdirectory(initialdir='D:\\',title='Select Directory')
        directory = dir_
        listDir.runCode(dir_)
        #os.chdir(dir_)
        # dir_files = os.listdir(dir_)
        # for file in dir_files:
        #     exten = file.split('.')[-1]
        #     for ex in music_ex:
        #         if exten == ex:
        #             print(file)
    
    def abrirMusica(self):
        dir_ = filedialog.askopenfilename(initialdir='D:/',title='Select File')
        filename = dir_.split('/')[-1]
        cng_dir = dir_.split('/')[0:-1]
        cng_dir = '/'.join(cng_dir)
        cng_dir = cng_dir + '/'
        #os.chdir(cng_dir)
        #filename = os.path.basename(dir_)
        print(dir_, cng_dir, '----' ,filename, filename[-3:])
        sample_db.add(filename, cng_dir, filename[-3:], 'mac', cdate)
        

class TagPage:
    

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        #self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        #self.quitButton.pack()


        #top = Toplevel()
        #top.title("Anexo")
        #Label(top, text="Name").grid(row=0, column=0, columnspan=2)

        global lbTag, nameTagEntry, nameTag, cdate

        cdate = date.today().strftime("%d/%m/%Y")

        nameLabel = Label(self.frame,text="Name")
        nameLabel.grid(row=0,column=0,columnspan=2)

        lbTag = Listbox(self.frame, height=20, width=94)
        lbTag.grid(row=6, column=0, columnspan=6)

        sbTag=Scrollbar(self.frame)
        sbTag.grid(row=6,column=6,rowspan=6)

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
            index=lbTag.curselection()[0]
            selectedTupleTag = lbTag.get(index)
            #nameTagEntry.delete(0,END)
            nameTagEntry.insert(END,selectedTupleTag[1])
        except IndexError:
            pass

    def view_commandTag(self):
        lbTag.delete(0,END)
        for row in tag_db.viewall():
            lbTag.insert(END,row)
    

    def search_commandTag(self):
        lbTag.delete(0,END)
        for row in tag_db.search(name= nameTag.get()):
            lbTag.insert(END,row)

    def add_commandTag(self):
        tag_db.add(nameTag.get(), cdate)
        lbTag.delete(0,END)
        lbTag.insert(END,nameTag.get(),cdate)


    def update_commandTag(self):
        tag_db.update(selectedTupleTag[0], nameTag.get(), cdate)
        self.view_command()

    def delete_commandTag(self):
        tag_db.delete(selectedTupleTag[0])
        self.view_command()

    def clear_commandTag(self):
        lbTag.delete(0,END)
        nameTagEntry.delete(0,END)



    def close_windows(self):
        self.master.destroy()

def main():
    #root = tk.Tk()
    #app = samplePage(root)
    #root.mainloop()
    samplePage('')
if __name__ == '__main__':
    main()

#interface = samplePage()
