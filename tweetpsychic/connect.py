from classifier_manager import Manager
import json

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/get_category',methods=['GET','POST'])
def get_category():
    handler = request.args.get('tweeterhandler')
    print handler
    global obj
    obj = Manager(handler)
    gender= obj.return_category()
    return jsonify(status=200,gender=gender)

if __name__ == '__main__':
    global ids
    ids = []
    app.run()
