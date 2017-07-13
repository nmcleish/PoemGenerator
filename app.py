from math import ceil
from data_manager import DataManager
from flask import Flask, render_template, request, flash, redirect, url_for, make_response, send_from_directory
from forms import PoemForm, FeelForm
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'development key'
port = int(os.getenv('PORT', 8080))

UPLOAD_FOLDER = 'save/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    form = FeelForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('user.html', form=form)

        feelings = form.feelings.data
        if form.domemotion.data:
            tones = datamanager.dom_emotion(feelings)
        else:
            tones = datamanager.calc_tones(feelings)

        if tones[6] == 'true':
            flash("Tell me a little bit more about how you're feeling.")
            return render_template('user.html', form=form)

        newpoem = datamanager.create_poem(tones, feelings, form.replacewords.data, form.select_or.data,
                                          form.no_fillers.data)

        if newpoem == None:
            if form.replacewords.data:
                flash("Word Replacement didn't work.")
            if form.select_or.data:
                flash("Shared Emotions didn't work.")
            return render_template('user.html', form=form)
        newpoem = newpoem.split('\n')
        return render_template('user.html', form=form, feelings=newpoem)

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

            line = form.line.data
            if len(line) < 10:
                flash("This line is too short.")
                return render_template('poem.html', form=form)
            tones = datamanager.add_line(line)
            if tones == None:
                flash("This line has already been added.")
                return render_template('poem.html', form=form)
            etones = []
            notes = ""
            if tones[6] == 'false':
                etones = ['Anger: ', 'Disgust: ', 'Fear: ', 'Joy: ', 'Sadness: ']
                for x in range(1, 6):
                    etones[x - 1] = etones[x - 1] + str(tones[x]).capitalize()
            else:
                notes = "Note: This has been marked as a filler."

            return render_template('submitted.html', line=line, etones=etones, notes=notes)

    elif request.method == 'GET':
        return render_template('poem.html', form=form)


@app.route('/data', methods=['GET', 'POST'])
@app.route('/data/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/data/<int:page>', methods=['GET', 'POST'])
def data5(page):
    data = datamanager.get_data()
    length = len(data)
    if request.method == 'POST':
        if "submit" in request.form:
            return edit(page)
    if length == 0:
        flash("Please add lines to view lines.")
        return redirect(url_for('admin'))
    prv = page - 1
    nxt = page + 1
    if page == 1:
        prv = int(ceil(length / 25.0))
    if ceil(length / 25.0) == page:
        nxt = 1
    data = data[(page - 1) * 25:page * 25]
    return render_template('data.html', data=data, len=len(data), nxt=nxt, prv=prv, page=page)


@app.route('/data/edit', methods=['GET', 'POST'])
def edit():
    if "save" in request.form:
        if request.form['save'] == "Delete Line":
            datamanager.delete_item(request.form["id"])
        else:
            i = int(request.form["id"])
            item = datamanager.get_item(i)
            val = request.form['new_line']
            if val != str(item[1]):
                datamanager.update_item(val, i)
        return redirect(url_for('data5'))
    x = request.form['submit']
    item = datamanager.get_item(int(x))
    return render_template('item.html', item=item, len=len(item))


@app.route('/save', methods=['GET', 'POST'])
def import_export():
    if request.method == 'POST':
        if request.form["submit"] == "Export":
            datamanager.getlines()
            return render_template("save.html")
        if 'file' not in request.files:
            return render_template('batch.html')
        file = request.files['file']
        if file.filename == '':
            flash('Please select a file.')
        if file and not allowed_file(file.filename):
            flash('Only .csv files can be imported.')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(datamanager.fill_db("save/" + filename))
            os.remove("save/" + filename)
            return redirect(url_for('admin'))

    return render_template('batch.html')


@app.route('/lines.csv', methods=['GET', 'POST'])
def download():
    datamanager.getlines()
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename="lines.csv")


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    if request.method == 'POST':
        if request.form["submit"] == "Yes":
            datamanager.clear_db()
            flash("All lines have been removed.")
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('admin'))
    return render_template('clear.html')


if __name__ == '__main__':
    # try:
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    datamanager = DataManager(
        os.environ.get('UNDERSTANDING_USERNAME'),
        os.environ.get('UNDERSTANDING_PASSWORD'),
        os.environ.get('ANALYZER_USERNAME'),
        os.environ.get('ANALYZER_PASSWORD'),
        os.environ.get('POSTGRESQL_USERNAME'),
        os.environ.get('POSTGRESQL_PASSWORD'),
        os.environ.get('POSTGRESQL_HOST'),
        os.environ.get('POSTGRESQL_DBNAME'),
        os.environ.get('POSTGRESQL_PORT'), )

    datamanager.init()
    app.run(host='0.0.0.0', port=port, debug=True)
