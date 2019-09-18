import sqlite3
def create():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tag(id_tag INTEGER PRIMARY KEY,name TEXT, date TEXT)")
    con.commit()
    con.close()

def viewall():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM tag Order By name ASC")
    rows = cur.fetchall()
    con.close()
    #print(rows)
    return rows

def viewMostUsed():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT t.id_tag, t.name, count(t.id_tag) as qtdUsage FROM tag as t inner join fato as f on t.id_tag = f.id_tag GROUP BY t.id_tag \
    UNION \
    SELECT t1.id_tag, t1.name , 0 from tag as t1 where t1.id_tag not in (SELECT id_tag from fato) \
    ORDER by qtdUsage DESC, name ")
    rows = cur.fetchall()
    con.close()
    return rows

def viewLastUsed():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT t.id_tag, t.name, max(f.date) as date FROM tag as t inner join fato as f on t.id_tag = f.id_tag GROUP BY t.name ORDER BY  f.date DESC")
    rows = cur.fetchall()
    con.close()
    return rows

def add(name, date):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("INSERT INTO tag VALUES(NULL,?,?)",(name,date))
    con.commit()
    con.close()

def addIfNotExist(name, date):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("insert into tag (name, date) Select ?, ? Where not exists(select * from tag where name=?)",(name,date,name))
    con.commit()
    con.close()

    

def delete(id):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("DELETE FROM tag WHERE id_tag=?",(id,))
    con.commit()
    con.close()

def update(id,name,cdate):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE tag SET name=?,date=? WHERE id_tag=?",(name,cdate,id))
    con.commit()
    con.close()

def search(name):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    print(name)
    cur.execute("SELECT * FROM tag WHERE name LIKE ?",('%'+name+'%',))
    rows = cur.fetchall()
    con.close()
    return rows

#Create a DB
create()
