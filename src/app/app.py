import sqlite3
from flask import Flask, request, jsonify, abort, g
import typing as tp

DATABASE = 'links.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception: BaseException | None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        f: tp.IO[tp.Any]
        with app.open_resource('schema.sql', mode='r') as f: # type: ignore 
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/goto/<shortname>', methods=['GET'])
def goto_url(shortname: str):
    if not shortname:
        abort(400, description="Missing 'shortname' parameter")

    db = get_db()
    cur = db.execute('SELECT full_url FROM links WHERE shortname = ?', (shortname,))
    row = cur.fetchone()
    cur.close()

    if row:
        return jsonify({"full_url": row['full_url']})
    else:
        abort(404, description=f"Shortname '{shortname}' not found")

@app.route('/link', methods=['POST'])
def link_url():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON data")

    shortname = data.get('shortname')
    full_url = data.get('full_url')

    if not shortname or not full_url:
        abort(400, description="Missing 'shortname' or 'full_url' in request body")

    db = get_db()
    try:
        db.execute('INSERT INTO links (shortname, full_url) VALUES (?, ?)', (shortname, full_url))
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        abort(409, description=f"Shortname '{shortname}' already exists.")
    
    return jsonify({"message": f"Shortname '{shortname}' linked to '{full_url}' successfully"}), 201

@app.route('/links', methods=['GET'])
def get_links():
    db = get_db()
    cur = db.execute('SELECT shortname, full_url FROM links')
    links = cur.fetchall()
    cur.close()
    return jsonify([dict(link) for link in links])
