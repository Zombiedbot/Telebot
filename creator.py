import sqlite3
import config

conn = sqlite3.connect(config.stats_name)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE players
                  ('Player', 'right', 'wrong')
               """)
