from flask import Flask
from flask import Flask, jsonify, request 
app = Flask(__name__)


@app.route('/',methods = ['POST','GET'])
def hello_world():
    if request.method == 'GET':
        return jsonify({'data': 'Hello world'}) 



@app.route('/fetchdata',methods = ['POST'])
def fetch():
    if request.method == 'POST':
        name = request.form.get("Name")
        company = request.form.get("Company")
        phone = request.form.get("Phone")
        print(name,company,phone)
        return jsonify({'Name': name,'company':company}) 


if __name__ == '__main__':
    app.run()