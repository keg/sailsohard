import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, url_for
app = Flask(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'sailsohard.db'),
    DEBUG=True
))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geo-json.js')
def geoJson():
    db = sqlite3.connect(app.config['DATABASE'])
    cur = db.execute('select id, latitude, longitude from messages')
    messages = cur.fetchall()
    return render_template('geo_json.html', messages=messages)

if __name__ == '__main__':
    app.run()