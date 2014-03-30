#!/usr/bin/env python 

from flask import request

from flask import Flask, url_for, render_template

app=Flask(__name__)
with app.test_request_context('/magic', method='POST'):
    print request.path
    print request.method
   

@app.route('/') 
def index():
    return "Index Pze"

@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None):
    return render_template('hello.html', name=username)

@app.route('/mello/')
def mello():
    return url_for('static', filename='mobil.css') 




if __name__ == '__main__':
    app.host='0.0.0.0'
    app.debug = True
    app.run()

