# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import (Flask, render_template, Response, request,
	Blueprint, redirect, send_from_directory, send_file, jsonify,
	g, url_for, flash)
import os
from classify import classified


app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/how')
def how_we_do():
	return app.send_static_file('how_we_do.html')

@app.route('/who')
def who_we_are():
	return app.send_static_file('who_we_are.html')
	
@app.route('/telling', methods = ['POST'])
def tell():
	handle = request.form['twitterHandle']
	print handle
#	py_obj=classified(handle)
#	json_string = classified(handle)
#	py_obj = json.loads(json_string)
	py_obj = classified(handle)
	print "object gotten"
	#age = "Over 25"
	#gender= "female"
	#wordcloud="static/images/JohnMayer_cloud.png"
	#py_obj = [age, gender, wordcloud]
#	interests = py_obj[2]
	gender = py_obj[1]
	age=py_obj[0]
#	json_string = json.dumps(py_obj)
	print gender, age
	if gender == 'female':
		return render_template('female.html', py_obj= py_obj) 
	else:
		return render_template('male.html', py_obj= py_obj)

port = os.getenv('VCAP_APP_PORT', '5000')
host = os.getenv('VCAP_APP_HOST', 'localhost')
print "I am running on port "+str(port)
print "The host is "+str(host)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))