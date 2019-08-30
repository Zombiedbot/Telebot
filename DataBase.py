import sqlite3

class DBase:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def stats(self, user):
        with self.connection:
            L = self.cursor.execute('SELECT * FROM players WHERE Player = ?', [(user)]).fetchall()
            return int(L[0][1]), int(L[0][2])
    
    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)
        
    def set_ans(self, user, r, w):
        rr, ww = self.stats(user)
        with self.connection:
            self.cursor.execute("""
                                UPDATE players
                                SET right = ?
                                WHERE Player = ?
                                """, (str(rr + r), user))
            self.cursor.execute("""
                                UPDATE players
                                SET wrong = ?
                                WHERE Player = ?
                                """, (str(ww + w), user))
    def set_user(self, user):
        with self.connection:
            s = self.cursor.execute('SELECT * FROM players WHERE Player = ?', [(user)]).fetchall()
            if not s:
                self.cursor.execute("""
                    INSERT INTO players
                    VALUES (?, '0', '0')
                    """, [(user)])

    def close(self):
        self.connection.close()
