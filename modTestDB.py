import sqlite3
from datetime import date

def printTable(table):
    for i in table:
        print(i)

def verifyIdNull():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("select id_sample from fato where id_sample is NULL")
    rows = cur.fetchall()
    printTable(rows)
    con.close()
    return

def missingIdTag():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("select * from (select f.id_tag as id_tag_fato, t.id_tag as id_tag_tag\
                from fato as f left join tag as t on f.id_tag = t.id_tag \
                where f.id_tag is not NULL and f.id_tag <> '' order by f.id_tag ) where id_tag_tag is NULL")
    rows = cur.fetchall()
    con.close()
    printTable(rows)
    if len(rows) != 0:
        return True
    return False

def missingIdSample():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("select * from ( select f.id_sample as id_sample_fato, s.id_sample as id_sample_sample \
                    from fato as f left join sample as s on f.id_sample = s.id_sample \
                    where f.id_sample is not NULL and f.id_sample <> '' order by f.id_sample ) where id_sample_sample is NULL")
    rows = cur.fetchall()
    printTable(rows)
    con.close()
    if len(rows) != 0:
        return True
    return False

    return

def noNameSample():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("select id_sample from sample where name is NULL")
    rows = cur.fetchall()
    printTable(rows)
    con.close()
    return


missingIdTag()

missingIdSample()

noNameSample()