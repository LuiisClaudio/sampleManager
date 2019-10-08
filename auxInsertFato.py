import sqlite3
import sample_db
import fato_db
import indexs
from random import choice
from datetime import date

def updateSample():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    querySample = sample_db.viewall()
    for row in querySample:
        print(row)
        #print(choice(indexs.lstBpm), choice(indexs.lstKey), choice(indexs.lstGenre))
        #print(row[0])
        #cur.execute("UPDATE sample SET bpm=?, key=?, genre=? WHERE id_sample=?",(choice(indexs.lstBpm), choice(indexs.lstKey), choice(indexs.lstGenre), row[0]))
    con.commit()
    con.close()

def updateFato():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    querySample = fato_db.viewall()
    for row in querySample:
        #print(row)
        #print( row[0], choice(range(101) ))
        #print(row[0])
        cur.execute("UPDATE fato SET love=? WHERE id_fato=?",(choice(range(101)), row[0]))
    con.commit()
    con.close()

updateFato()