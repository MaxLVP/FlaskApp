from flask import Flask, render_template, request
import sqlite3


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

with UseDatabase('appdatabase.db') as cursor:

    cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, phrase text, letters text, ip text, browser_string text, results text)")


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

app.run(debug=True)





