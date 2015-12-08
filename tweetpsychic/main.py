import json
# We'll render HTML templates and access data sent by GET
# using the request object from flask. jsonify is required
# to send JSON as a response of a request
from flask import Flask, render_template, request, redirect, jsonify
import getTweets
 

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telling', methods = ['POST'])
def female():
	handle = request.form['twitterHandle']
	print handle
	getTweets.tweets(handle)
	return render_template('female.html')

"""
	if ...:
	  	return render_template('male.html')
"""
@app.route('/how')
def how_we_do():
	return render_template('how_we_do.html')

@app.route('/who')
def who_we_are():
	return render_template('who_we_are.html')

if __name__ == '__main__':
	app.run()



