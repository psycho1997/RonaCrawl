from flask import Flask, render_template, jsonify, send_from_directory, request, redirect
import flask
from shelljob import proc
import os
import sys


app = Flask(__name__)
g = proc.Group()
p = g.run(["python3", "-u", "bot.py"])
dir = "logs"

@app.route('/')
def index():
    if 'start' in request.form:
        return redirect("google.com")
    elif 'stop' in request.form:
        print("stop", file=sys.stdout)
    return render_template('index.html')


@app.route( '/bot' )
def bot():
    def read_process():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line
    return flask.Response( read_process(), mimetype= 'text/plain' )

@app.route('/files')
def list_files():
    files = []
    for filename in os.listdir(dir):
        path = os.path.join(dir,filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/files/<path:path>")
def get_file(path):
    return send_from_directory(dir, path, as_attachment=True)