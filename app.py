from flask import Flask, render_template
import flask
from shelljob import proc

app = Flask(__name__)
g = proc.Group()
p = g.run(["python3", "-u", "bot.py"])


@app.route('/')
def index():
    return render_template('index.html')


@app.route( '/bot' )
def bot():
    def read_process():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

    return flask.Response( read_process(), mimetype= 'text/plain' )

