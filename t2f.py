import os.path
from flask import Flask, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import numpy as np

global max_index

app = Flask(__name__)
app.config['SECRET_KEY'] = '5UP3R53CR3TK3Y'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Dosyayı Yükle")


def process_text(file_path):
    given_file = open(file_path, "r")
    processed_file = open('./static/files/processed.txt', 'w')
    global max_index
    max_index = 0

    array_all_lines = []

    lines = given_file.readlines()
    for line in lines:
        processed_file.write(line[5:])

    processed_file.close()
    processed_file = open('./static/files/processed.txt', 'r')

    for line in processed_file:
        array_line = []
        for char in line:
            array_line.append(char)

        array_all_lines.append(array_line)

        if len(line) > max_index:
            max_index = len(line)

    for line in array_all_lines:
        if len(line) < max_index:
            for i in range(max_index-len(line)):
                line.append(' ')

    given_file.close()
    processed_file.close()
    matrix = np. array(array_all_lines)
    return matrix


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename('given.txt')))
        return redirect(url_for("result"))
    return render_template('index.html', form=form)


@app.route('/result')
def result():
    global max_index
    datas = process_text('./static/files/given.txt')
    return render_template('result.html', datas=datas, max_index=max_index)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)
