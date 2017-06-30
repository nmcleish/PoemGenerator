from math import ceil
from data_manager import DataManager
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import PoemForm, FeelForm
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = 'development key'


@app.route("/", methods=['GET', 'POST'])
def index():
    form = FeelForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('user.html', form=form)
        feelings = form.feelings.data
        tones = datamanager.calc_tones(feelings)
        if tones[6] == 'true':
            flash("Tell me a little bit more about how you're feeling.")
            return render_template('user.html', form=form)
        data = datamanager.create_poem(tones, feelings, form.replacewords.data).split('\n')
        return render_template('user.html', form=form, feelings=data)

    if request.method == 'GET':
        return render_template('user.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')


@app.route('/poem', methods=['GET', 'POST'])
def poem():
    form = PoemForm()

    if request.method == 'POST':
        if form.cancel.data:
            return render_template('admin.html')
        if form.validate() == False:
            return render_template('poem.html', form=form)
        else:

            line = form.line.data.lower().capitalize()
            tones = datamanager.add_line(line)
            etones = []
            notes = ""
            if tones[6] == 'false':
                etones = ['Anger: ', 'Disgust: ', 'Fear: ', 'Joy: ', 'Sadness: ']
                for x in range(1, 6):
                    etones[x - 1] = etones[x - 1] + str(tones[x])
            else:
                notes = "Note: This has been marked as a filler."

            return render_template('submitted.html', line=line, etones=etones, notes=notes)

    elif request.method == 'GET':
        return render_template('poem.html', form=form)


@app.route('/data', methods=['GET', 'POST'])
@app.route('/data/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/data/<int:page>', methods=['GET', 'POST'])
def data5(page):
    print request.form
    data = datamanager.get_data()
    length = len(data)
    print length
    if request.method == 'POST':
        if "submit" in request.form:
            return edit(page)
    prv = page - 1
    nxt = page + 1
    if page == 1:
        prv = int(ceil(length / 25.0))
        print "prev caught"
    if ceil(length / 25.0) == page:
        nxt = 1
        print "end caught"
    data = data[(page - 1) * 25:page * 25]
    return render_template('data.html', data=data, len=len(data), nxt=nxt, prv=prv, page=page)


@app.route('/data/edit', methods=['GET', 'POST'])
def edit():
    print request.form
    if "save" in request.form:
        if request.form['save'] == "Delete Line":
            datamanager.delete_item(request.form["id"])
            print 'deleted'
        else:
            i = int(request.form["id"])
            print i
            item = datamanager.get_item(i)
            print item
            val = request.form['new_line']
            print val
            print "yyyyy"
            if val != str(item[1]):
                print "Test"
                datamanager.update_item(val, i)
        return redirect(url_for('data5'))
    x = request.form['submit']
    item = datamanager.get_item(int(x))
    return render_template('item.html', item=item, len=len(item))


if __name__ == '__main__':
    try:
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
        datamanager = DataManager(
            os.environ.get('UNDERSTANDING_USERNAME'),
            os.environ.get('UNDERSTANDING_USERNAME'),
            os.environ.get('ANALYZER_USERNAME'),
            os.environ.get('ANALYZER_PASSWORD'),
            os.environ.get('POSTGRESQL_USERNAME'),
            os.environ.get('POSTGRESQL_PASSWORD'),
            os.environ.get('POSTGRESQL_HOST'),
            os.environ.get('POSTGRESQL_DBNAME'),)
        datamanager.init()
        app.run(debug=True)
    except:
        print "Didn't Work"
