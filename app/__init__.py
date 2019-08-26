from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
from werkzeug.utils import secure_filename
from app.models.md_convertions import convert_target

# Configurations



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config.from_object('config')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = convert_target(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('area_select',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/area_select', methods=['GET'])
def area_select():
    filename = request.args.get('filename')
    filename = url_for('static', filename=f'contratos_img/{filename}/{filename}_0.jpg')
    print(filename)
    return render_template('index.html', filename=filename)

