import sqlite3
db = sqlite3.connect("Uplift.db")

db.execute("""
create table if not exists Users (
    Email varchar(32) primary key,
    FName varchar(32) not null,
    LName varchar(32) not null,
    PhoneNumber varchar(20) not null
);
""")

db.execute("""
create table if not exists Replies (
    ReplyID integer primary key autoincrement,
    Email varchar(32) not null,
    Data varchar(255) not null,
    constraint fk_Replies_Users
        foreign key (Email)
        references Users (Email)
);
""")