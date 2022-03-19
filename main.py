from flask import Flask, render_template, request, session
import sqlite3
from checker import check_logged_in


class UseDatabase:

    def __init__(self, file='appdatabase.db'):
        self.file = file

    def __enter__(self):
        self.con = sqlite3.connect(self.file)
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.cursor.close()
        self.con.close()


app = Flask(__name__)
app.secret_key = 'YouWillNeverGuessSecretKey'

with UseDatabase('appdatabase.db') as cursor:

    cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, phrase text, letters text, ip text, browser_string text, results text)")


@app.route('/login')
def do_login():
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    return 'You are now logged out.'


def log_request(req, res):
    with UseDatabase('appdatabase.db') as cursor:
        _SQL = """insert into users (phrase, letters, ip, browser_string, results)
        values
        (?, ?, ?, ?, ?)"""
        cursor.execute(_SQL, (req.form['phrase'],
                       req.form['letters'],
                       req.remote_addr,
                       req.user_agent.browser,
                       res, ))


@app.route('/')
def hello() -> str:
    return 'Hello world from flask'


@app.route('/search', methods=['POST'])
def search4letters() -> set:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are you results'
    results = str(set(letters).intersection(set(phrase)))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)



@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search App on the web')


@app.route('/viewlog')
@check_logged_in
def view_the_log():
    with UseDatabase('appdatabase.db') as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results from users"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents, )


if __name__ == '__main__':
    app.run(debug=True)





