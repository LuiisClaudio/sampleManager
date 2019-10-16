import sqlite3
def create():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sample(id_sample INTEGER PRIMARY KEY,name TEXT,path TEXT, extension TEXT,disk TEXT, date TEXT)")
    con.commit()
    con.close()

def viewall():
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM sample")
    rows = cur.fetchall()
    con.close()
    return rows

def add(name,path,extension,disk,date):
    con = sqlite3.connect("sample_db.db", timeout=10)
    cur = con.cursor()
    cur.execute("INSERT INTO sample VALUES(NULL,?,?,?,?,?, NULL, NULL, NULL)",(name,path,extension,disk,date))
    con.commit()
    con.close()

def delete(id):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("DELETE FROM sample WHERE id_sample=?",(id,))
    con.commit()
    con.close()

def search(name="",path="",extension="",disk="", lstAndOr=""):
    print(lstAndOr)
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    nameWhere = " name LIKE ? "
    pathWhere = " path LIKE ? "
    extensionWhere = " extension LIKE ? "
    diskWhere = " disk LIKE ? "
    query = "SELECT * FROM sample WHERE " + nameWhere + lstAndOr[0] + pathWhere + lstAndOr[1] + extensionWhere + lstAndOr[2] + diskWhere
    print(query)
    #cur.execute("SELECT * FROM sample WHERE name LIKE ? OR path LIKE ? OR extension LIKE ? OR disk LIKE ?", (name if name == "" else "%"+name+"%", lstAndOr[0] ,path if path == "" else  "%"+path+"%", lstAndOr[1] ,extension, lstAndOr[2] ,disk))#,"%"+extension+"%","%"+disk+"%"))
    cur.execute(query, (name if name == "" else "%" + name + "%", path if path == "" else "%" + path + "%", extension, disk))  # ,"%"+extension+"%","%"+disk+"%"))
    rows = cur.fetchall()
    con.close()
    return rows

def update(id,name,path,extension,disk,date):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE sample SET name=?,path=?,extension=?,disk=?,date=? WHERE id_sample=?",(name,path,extension,disk,date,id))
    con.commit()
    con.close()

def updateByInterface(id_sample, bpm, key, genre):
    con = sqlite3.connect("sample_db.db")
    cur = con.cursor()
    cur.execute("UPDATE sample SET bpm=?, key=?, genre=? WHERE id_sample=?",(bpm, key, genre, id_sample) )
    con.commit()
    con.close()

#Create a DB
create()
