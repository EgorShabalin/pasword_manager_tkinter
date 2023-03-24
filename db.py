import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Passwords (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, password TEXT)"
        )
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM Passwords")
        rows = self.cur.fetchall()
        return rows

    def save(self, name, psw):
        self.cur.execute(
            "INSERT INTO Passwords(name, password) VALUES (?,?)", (str(name), str(psw))
        )
        self.conn.commit()

    def delete(self, index):
        self.cur.execute("DELETE FROM Passwords WHERE id=?", (str(index),))
        self.conn.commit()

    def copy(self, index):
        self.cur.execute("SELECT password FROM Passwords WHERE id=?", (str(index),))
        c = self.cur.fetchall()
        return str(c[0][0])

    def __del__(self):  # closes sql connection
        self.conn.close()


data = Database()
