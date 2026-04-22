import sqlite3
try:
    db = sqlite3.connect("Uplift.db")
    db.execute("pragma foreign_keys = on")
    db.executescript(open("Uplift.sql", "rt").read())
    db.commit()
    print("Database loaded!")
except:
    print("Database could not be loaded.")