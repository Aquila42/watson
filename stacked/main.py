import json
# We'll render HTML templates and access data sent by GET
# using the request object from flask. jsonify is required
# to send JSON as a response of a request
from flask import Flask, render_template, request, redirect, jsonify
# import getTweets
from classify import classified

# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def tell():
    handle = request.form['twitterHandle']
    print(handle)
    py_obj = classified(handle)
    gender = py_obj[2]
    if gender == 'female':
        return render_template('female.html', py_obj=py_obj)
    else:
        return render_template('male.html', py_obj=py_obj)

@app.route('/how')
def how_we_do():
    return render_template('how_it_works.html')


@app.route('/who')
def who_we_are():
    return render_template('who_we_are.html')

@app.errorhandler(500)
def pageNotFound(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run()
