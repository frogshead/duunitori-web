import sqlite3

from flask import Flask, g, render_template, json
app = Flask(__name__)

DATABASE = '/Users/mikko/ohjelmointi/github/duunitori/duunitori/duunitori.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query,args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/list")
def list():
    _rows = query_db("SELECT company, title, url FROM duunit ORDER BY company")
    rows = [dict(title = row[1], company = row[0], url = row[2]) for row in _rows] 
    return render_template("list.html", rows = rows)

@app.route("/list/json")
def list_json():
    _rows = query_db("SELECT company, title, url FROM duunit ORDER BY company")
    rows = [dict(title = row[1], company = row[0], url = row[2]) for row in _rows] 
    return json.jsonify(rows)

 