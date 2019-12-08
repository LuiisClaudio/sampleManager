import sqlite3
from datetime import date

def inicializaFato():
    con = sqlite3.connect("sample_db.db", timeout=10)
    cur = con.cursor()
    cur.execute("SELECT * FROM sample")
    rows = cur.fetchall()
    for i in rows:
        cur.execute("INSERT INTO fato VALUES(NULL,?,?)",(i[0],""))
    con.commit()
    con.close()

def selectAll():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT f.id_fato, s.id_sample, s.name, s.path, s.extension, s.disk, t.id_tag, ifnull(t.name, '-') as tag, s.bpm, s.key, s.genre, f.love \
    FROM fato as f INNER JOIN sample as s on f.id_sample = s.id_sample LEFT JOIN tag as t on f.id_tag = t.id_tag \
    Order By s.name ASC -- , t.name ASC")
    rows = cur.fetchall()
    con.close()
    return rows


def selectFilter(name="",path="",extension="",disk="", tag="", bpm="", key="", genre = "", loveLow = "", loveUpper = ""):
    lstParam = []
    nameWhere = ""
    pathWhere = ""
    extensionWhere = ""
    diskWhere = ""
    tagWhere = ""
    bpmWhere = ""
    keyWhere = ""
    genreWhere = ""
    where = " Where "
    if name != "":
        nameWhere = ' s.name LIKE ? AND '
        lstParam.append(name) 
        where = where + nameWhere
    if path != "":
        pathWhere = ' s.path LIKE ? AND '
        lstParam.append(path)
        where = where + pathWhere
    if extension != "":
        extensionWhere = ' s.extension LIKE ? AND '
        lstParam.append(extension) 
        where = where + extensionWhere
    if disk != "":
        diskWhere = ' s.disk LIKE ? AND '
        lstParam.append(disk) 
        where = where + diskWhere
    if tag != "":
        tagWhere = ' t.name LIKE ? AND '
        lstParam.append(tag)
        where = where + tagWhere
    if bpm != "":
        bpmWhere = ' s.bpm = ' + str(bpm) + ' AND '
        where = where + bpmWhere

    if key != "":
        keyWhere = ' s.key = ' + "'" + key + "'" + ' AND '
        where = where + keyWhere
    if genre != "":
        genreWhere = ' s.genre = '+ "'" + genre + "'" + ' AND '
        where = where + genreWhere

    if(loveUpper != "" or loveLow != ""):
        if loveUpper == "":
            loveUpper = loveLow
        elif loveLow == "":
            loveLow = loveUpper


        loveLowWhere = ' f.love >= ' + str(loveLow) + ' AND '

        where = where + loveLowWhere

        loveUpperWhere = ' f.love <= '+ str(loveUpper)  + ' AND '   

        where = where + loveUpperWhere

    where = where + ' 1 = 1'

    where = where + ' Order By s.name ASC '

    #print(where)


    
    con = sqlite3.connect("sample_db.db")

    #print("SELECT f.id_fato, s.id_sample, s.name, s.path, s.extension, s.disk, t.id_tag, ifnull(t.name, '-') as tag FROM fato as f INNER JOIN sample as s on f.id_sample = s.id_sample LEFT JOIN tag as t on f.id_tag = t.id_tag" + where)
    selectFrom = "SELECT f.id_fato, s.id_sample, s.name, s.path, s.extension, s.disk, t.id_tag, ifnull(t.name, '-') as tag, s.bpm, s.key, s.genre, f.love FROM fato as f INNER JOIN sample as s on f.id_sample = s.id_sample LEFT JOIN tag as t on f.id_tag = t.id_tag "
    cur = con.cursor()
    if len(lstParam) == 0:
        cur.execute(selectFrom + where)
    elif len(lstParam) == 1:
        cur.execute(selectFrom + where, ('%'+lstParam[0]+'%',))
    elif len(lstParam) == 2:
        cur.execute(selectFrom + where, ('%'+lstParam[0]+'%','%'+lstParam[0]+'%'))
    elif len(lstParam) == 3:
        cur.execute(selectFrom + where, ('%'+lstParam[0]+'%','%'+lstParam[1]+'%','%'+lstParam[2]+'%'))
    elif len(lstParam) == 4:
        cur.execute(selectFrom + where, ('%'+lstParam[0]+'%','%'+lstParam[1]+'%','%'+lstParam[2]+'%','%'+lstParam[3]+'%'))
    elif len(lstParam) == 5:
        cur.execute(selectFrom + where, ('%'+lstParam[0]+'%','%'+lstParam[1]+'%','%'+lstParam[2]+'%','%'+lstParam[3]+'%','%'+lstParam[4]+'%'))
    rows = cur.fetchall()

    #for i in rows:
    #     print(i)

    con.close()
    return rows

def create():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS fato(id_fato INTEGER PRIMARY KEY, id_sample INTEGER, id_tag INTEGER, love INTEGER, date TEXT, date_sample_mod TEXT, date_tag_mod TEXT)")
    con.commit()
    con.close()

def viewall():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM fato")
    rows = cur.fetchall()
    con.close()
    return rows

def add(id_sample,id_tag):
    con = sqlite3.connect("sample_db.db", timeout=10)
    cur = con.cursor()
    cur.execute("INSERT INTO fato VALUES(NULL,?,?)",(id_sample,id_tag))
    con.commit()
    con.close()

def addIfNotExist(id_sample,id_tag):
    con = sqlite3.connect("sample_db.db", timeout=10)
    cur = con.cursor()
    cur.execute("insert into fato (id_sample, id_tag, date) Select ?, ?, ? Where not exists(select * from fato where id_sample=? and id_tag=?)",(id_sample,id_tag, date.today().strftime("%d/%m/%Y"),id_sample,id_tag))
    con.commit()
    con.close()

def addSampleIfNotExist(id_sample):
    con = sqlite3.connect("sample_db.db", timeout=10)
    cur = con.cursor()
    cur.execute("insert into fato (id_sample, date) Select ?, ? Where not exists(select * from fato where id_sample=?)",(id_sample, date.today().strftime("%d/%m/%Y"),id_sample))
    con.commit()
    con.close()

def addTag(id_sample, id_tag):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("INSERT INTO fato VALUES(NULL,?,?,?)",(id_sample,id_tag, date.today().strftime("%d/%m/%Y")))
    con.commit()
    con.close()

def delete(id):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("DELETE FROM fato WHERE id_fato=?",(id,))
    con.commit()
    con.close()

def search():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM sample WHERE id_fato = ?",(id,))
    rows = cur.fetchall()
    con.close()
    return rows

def update(id_fato, id_sample, id_tag):
    con = sqlite3.connect("sample_db.db", isolation_level=None)
    cur = con.cursor()
    cur.execute("UPDATE fato SET id_sample=?,id_tag=? WHERE id_fato=?", (id_sample, id_tag, id_fato))
    con.commit()
    con.close()


def updateSample(id,id_sample):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE fato SET id_sample=? and data_sample_mod=? WHERE id_fato=?",(id_sample, date.today().strftime("%d/%m/%Y"), id))
    con.commit()
    con.close()

def updateTag(id, id_tag):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE fato SET id_tag=?, date_tag_mod=? WHERE id_fato=?",(id_tag, date.today().strftime("%d/%m/%Y"),id))
    con.commit()
    con.close()

def updateByInterface(id_fato, id_sample, love, id_tag):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    if love != '':
        cur.execute("UPDATE fato SET love=?, date_sample_mod=? WHERE id_sample=?",(love, date.today().strftime("%d/%m/%Y"), id_sample) )
    else:
        cur.execute("UPDATE fato SET love=NULL, date_sample_mod=? WHERE id_sample=?", (date.today().strftime("%d/%m/%Y"), id_sample))
    if id_tag != None:
        cur.execute("UPDATE fato SET id_tag=? WHERE id_fato=?", (id_tag, id_sample))
    con.commit()
    con.close()

def removeTagFato(id_tag):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE fato SET id_tag=NULL WHERE id_tag=?", (id_tag,))
    con.commit()
    con.close()

def removeTagFatoRow(id_fato, id_tag):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE fato SET id_tag=NULL and date_tag_mod=? WHERE id_fato=? and id_tag=?", (date.today().strftime("%d/%m/%Y"), id_fato, id_tag))
    con.commit()
    con.close()

#Create a DB
create()
#inicializaFato()

#selectFilter('drums','drums','wav','mac','')
