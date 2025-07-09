from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user'] = username
            flash('Login successful.')
            return redirect('/dashboard')
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect('/login')
    conn = get_db_connection()
    trains = conn.execute('SELECT * FROM trains').fetchall()
    conn.close()
    return render_template('dashboard.html', trains=trains)

@app.route('/book/<int:train_id>')
def book(train_id):
    if 'user' not in session:
        return redirect('/login')
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (username, train_id) VALUES (?, ?)', (session['user'], train_id))
    conn.commit()
    conn.close()
    flash('Ticket booked successfully.')
    return redirect('/dashboard')

@app.route('/cancel/<int:booking_id>')
def cancel(booking_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
    conn.commit()
    conn.close()
    flash('Booking cancelled.')
    return redirect('/mybookings')

@app.route('/mybookings')
def mybookings():
    if 'user' not in session:
        return redirect('/login')
    conn = get_db_connection()
    bookings = conn.execute('SELECT b.id, t.name, t.source, t.destination FROM bookings b JOIN trains t ON b.train_id = t.id WHERE b.username = ?', (session['user'],)).fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        source = request.form['source']
        destination = request.form['destination']
        conn = get_db_connection()
        conn.execute('INSERT INTO trains (name, source, destination) VALUES (?, ?, ?)', (name, source, destination))
        conn.commit()
        conn.close()
        flash('Train added successfully.')
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        import create_db
    app.run(debug=True)
