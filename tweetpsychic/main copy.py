import json
# In this example we are going to create a simple HTML
# page with 2 input fields (numbers), and a link.
# Using jQuery we are going to send the content of both
# fields to a route on our application, which will
# sum up both numbers and return the result.
# Again using jQuery we'll show the result on the page


# We'll render HTML templates and access data sent by GET
# using the request object from flask. jsonify is required
# to send JSON as a response of a request
from flask import Flask, render_template, request, redirect, jsonify
import getTweets
 

# Initialize the Flask application
app = Flask(__name__)


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
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

if __name__ == '__main__':
	app.run()



