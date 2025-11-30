# app.py
# Aplikasi Flask yang SENGAJA rentan untuk tujuan edukasi.
# Menampilkan contoh: IDOR, Privilege Escalation, Forced Browsing, Parameter Tampering.
#
# WARNING: Jangan jalankan di server publik. Hanya untuk lab lokal.

from flask import Flask, request, session, redirect, url_for, render_template, g, flash
import sqlite3
import os

APP_SECRET = "xinsecure-secret-for-demo-only"  # jangan gunakan di produksi

app = Flask(__name__)
app.secret_key = APP_SECRET
DATABASE = 'db.sqlite3'


# -----------------------
# Database helper
# -----------------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        exists = os.path.exists(DATABASE)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        if not exists:
            init_db(db)
    return db

def init_db(db):
    cur = db.cursor()
    # Users table: id (int), username, role, email, balance
    cur.executescript('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        email TEXT,
        balance REAL
    );

    INSERT INTO users (username, password, role, email, balance) VALUES
        ('alice', 'alicepass', 'user', 'alice@example.local', 100.0),
        ('bob',   'bobpass',   'user', 'bob@example.local', 250.0),
        ('carol', 'carolpass', 'admin','carol@example.local', 1000.0);
    ''')
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash("Anda harus login dulu", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

# -----------------------
# Simple auth (insecure, demo only)
# -----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        cur = get_db().execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        if user:
            # store user id and role in session (vulnerable to tampering if not protected)
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Logged in as {user['username']}")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "error")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('index'))


# -----------------------
# Public index
# -----------------------
@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = {'id': session.get('user_id'), 'username': session.get('username'), 'role': session.get('role')}
    return render_template('index.html', user=user)


@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')

    cur = get_db().execute(
        'SELECT id, username, email, balance FROM users WHERE id = ?',
        (user_id,)
    )
    row = cur.fetchone()

    if not row:
        flash("User not found", "error")
        return redirect(url_for('index'))

    return render_template('profile.html', profile=row)



@app.route('/admin')
@login_required
def admin_dashboard():
    if session['role'] != 'admin':
       flash("User not authorized", "error")
       return redirect(url_for('index'))

    cur = get_db().execute('SELECT id, username, role, email FROM users')
    users = cur.fetchall()
    return render_template('admin_dashboard.html', users=users)


@app.route('/become_admin', methods=['POST'])
@login_required
def become_admin():
    if session.get('role') != 'admin':
        flash("Unauthorized action!", "error")
        return redirect(url_for('index'))

    new_role = request.form.get('role', '').strip()
    target_user_id = request.form.get('user_id')

    valid_roles = ['user', 'admin']

    if new_role not in valid_roles:
        flash("Invalid role", "error")
        return redirect(url_for('admin_dashboard'))

    try:
        target_user_id = int(target_user_id) # type: ignore
    except:
        flash("Invalid user ID", "error")
        return redirect(url_for('admin_dashboard'))

    db = get_db()
    db.execute(
        'UPDATE users SET role = ? WHERE id = ?',
        (new_role, target_user_id)
    )
    db.commit()

    flash("Role updated securely")
    return redirect(url_for('admin_dashboard'))



@app.route('/billing')
@login_required
def billing():
    bill_id = request.args.get('bill_id')

    if not bill_id:
        flash("No bill_id provided", "error")
        return redirect(url_for('index'))

    try:
        requested_id = int(bill_id)
    except ValueError:
        flash("Invalid bill ID format", "error")
        return redirect(url_for('index'))

    current_user_id = session.get('user_id')

    # hanya boleh akses tagihan sendiri
    if requested_id != current_user_id:
        flash("Unauthorized access to billing data", "error")
        return redirect(url_for('index'))

    cur = get_db().execute(
        'SELECT id, username, email, balance FROM users WHERE id = ?',
        (requested_id,)
    )
    bill = cur.fetchone()

    if not bill:
        flash("Bill not found", "error")
        return redirect(url_for('index'))

    return render_template('billing.html', bill=bill)



@app.route('/users')
@login_required
def user_list():
    if session.get('role') != 'admin':
        flash("Admin only!", "error")
        return redirect(url_for('index'))

    cur = get_db().execute('SELECT id, username, role FROM users')
    rows = cur.fetchall()
    return render_template('user_list.html', users=rows)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
