from flask import g
import sqlite3

def connect_db():
    sql = sqlite3.connect('/home/codemask/Documents/FlaskProject/Member_API/members.db')
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
