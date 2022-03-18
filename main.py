from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'Hello world from flask'


@app.route('/search', methods=['POST'])
def search4letters() -> set:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are you results'
    results = str(set(letters).intersection(set(phrase)))
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search App on the web')


app.run(debug=True0)





