import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, url_for
app = Flask(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'sailsohard.db'),
    DEBUG=True
))

def get_data():
    db = sqlite3.connect(app.config['DATABASE'])
    cur = db.execute('select id, longitude, latitude from messages order by unixTime desc')
    messages = cur.fetchall()
    return messages

@app.route('/')
def index():
    return render_template('index.html', messages=get_data())

if __name__ == '__main__':
    app.run()
