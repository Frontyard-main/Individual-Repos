
from flask import Flask, jsonify, request 
app = Flask(__name__)

@app.route('/register',methods = ['POST'])
def hello_world():
        name = request.form.get('name')
        return jsonify({'name': name}) 

if __name__ == '__main__':
    app.run()