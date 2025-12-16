from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)




@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (content, done) VALUES (?, ?)', (task, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def done(id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET done = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()

    if request.method == 'POST':
        new_content = request.form['task']
        conn.execute(
            'UPDATE tasks SET content = ? WHERE id = ?',
            (new_content, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

        

    task = conn.execute(
        'SELECT * FROM tasks WHERE id = ?',
        (id,)
    ).fetchone()
    conn.close()

    return render_template('edit.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
