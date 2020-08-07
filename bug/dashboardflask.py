from flask import Flask, request, url_for, redirect, render_template,jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pending_request')
def pending_request():
    return "Entered pending request"
if __name__ == '__main__':
    app.run()