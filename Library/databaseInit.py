import sqlite3 as sql
from sqlite3 import Cursor

conn = sql.connect("books.db")


def create_book_table():
    conn.execute(
        "CREATE TABLE Library ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "author TEXT NOT NULL, "
        "pubyear INTEGER NOT NULL, "
        "publisher TEXT, desc TEXT)"
    )
    print("Table created")


def insert_test_data(cur: Cursor):
    cur.execute(
        "INSERT INTO Library (title, author, pubyear) VALUES (?, ?, ?)",
        ("Ace Attorney", "Edgeworth", 2013),
    )
    conn.commit()


def fetch_single(cur: Cursor):
    cur.execute("select * from Lib")
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    # create_book_table()
    cur = conn.cursor()
    insert_test_data(cur)
    fetch_single(cur)
    conn.close()
