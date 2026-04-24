import sqlite3
from flask import g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("Uplift.db")
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def addToUsers(Email, FName, LName, PhoneNumber):
    db = get_db()
    db.execute("""
    insert into Users (Email, FName, LName, PhoneNumber)
        values
        (?, ?, ?, ?)
    on conflict(Email) do update set
        FName = excluded.FName,
        LName = excluded.LName,
        PhoneNumber = excluded.PhoneNumber
    """, (Email, FName, LName, PhoneNumber))
    db.commit()

def addToReplies(Email, Data):
    db = get_db()
    db.execute("""
    insert into Replies (Email, Data)
        values
        (?, ?)
    """, (Email, Data))
    db.commit()

def setUserEmailAsInvalid(Email, PermanentlyInvalid):
    db = get_db()
    cursor = db.execute("""
    update Users
        set ValidEmail = 0, PermanentlyInvalid = ?
    where email = ?
    """, (PermanentlyInvalid, Email))
    if cursor.rowcount <= 0:
        print(f"No user found for email {Email}")
    db.commit()

def init_db():
    try:
        db = sqlite3.connect("Uplift.db")
        db.execute("pragma foreign_keys = on")
        db.executescript(open("Uplift.sql", "rt").read())
        db.commit()
        print("Database loaded!")
    except:
        print("Database could not be loaded.")

