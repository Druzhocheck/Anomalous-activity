from flask import Flask, request, render_template, redirect, url_for, session
import cgi
from werkzeug.utils import secure_filename
import os
import formating
import pandas as pd
import isolationforest
import json

app = Flask(__name__, static_folder="static")
form = cgi.FieldStorage()
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['log', 'txt', 'docs', 'docx', 'doc', 'json'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'anomalyevetsinoperatingsystemlinux'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['btn'] == 'collect':
            start = request.form.get('start').replace('T', ' ')
            end = request.form.get('end').replace('T', ' ')
            dataset = pd.DataFrame(formating.journalctl(start, end))
            anomaly_desciption = isolationforest.anomaly(dataset)
            session['data'] = anomaly_desciption.to_json()
            return redirect(url_for('analyzer'))

        elif request.form['btn'] == 'analyze':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                dataset = pd.DataFrame(formating.json_format(UPLOAD_FOLDER + "/" + filename))
                print(dataset)
                anomaly_desciption = isolationforest.anomaly(dataset)
                if os.path.isfile(UPLOAD_FOLDER + "/" + filename):
                    os.remove(UPLOAD_FOLDER + "/" + filename)
                session['data'] = anomaly_desciption.to_json()
                return redirect(url_for('analyzer'))
            
    return render_template('index.html')

@app.route("/analyzer")
def analyzer():
    mass = []
    data_description = json.loads(session.get('data'))["description"]
    data_cmdline = json.loads(session.get('data'))["_CMDLINE"]
    data_hostname = json.loads(session.get('data'))["_HOSTNAME"]
    data_syslog_timestamp = json.loads(session.get('data'))["SYSLOG_TIMESTAMP"]
    for i in data_description:
        mass.append(dict(timestamp=data_syslog_timestamp.get(i),hostname=data_hostname.get(i),event=data_cmdline.get(i),description=data_description.get(i)))
        
    return render_template('analyzer.html', anomaly_desciption=mass)


if __name__ == "__main__":
    # debug=True - вывод ошибок на страницу
    app.run(debug=True)
