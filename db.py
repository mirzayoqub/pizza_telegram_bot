import sqlite3

db = sqlite3.connect('user.db', check_same_thread=False)
cursor = db.cursor()
