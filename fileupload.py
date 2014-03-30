#!/usr/bin/python

from flask import Flask, request, redirect, url_for, render_template, redirect, send_from_directory
import time
from werkzeug.utils import secure_filename
import os
from os import listdir, path
from os.path import isdir, isfile, join



UPLOAD_FOLDER=os.path.abspath('uploads')


ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__) 



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename) :
    return '.' in filename and \
         filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


def getdirs(mypath) :
    retarr = []
    try :
        retarr = [ f for f in listdir(mypath) if isdir(join(mypath,f)) ]
    except :
        pass
    return(retarr) 

def getfiles(mypath) :
    retarr = [] 
    try :
        retarr = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    except : 
        pass
    return(retarr) 

@app.route('/', methods=['GET', 'POST']) 
def upload_file() :
    if request.method == 'POST' :
        file = request.files['file']
        if file and allowed_file(file.filename) :
            filename=secure_filename(file.filename)
            timestring = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).replace(':','-').replace(' ','-')
            os.mkdir(UPLOAD_FOLDER + '/' + timestring)
            abs_path = UPLOAD_FOLDER + '/' + timestring
            file.save(os.path.join(abs_path, filename))
            return redirect(url_for('uploaded_file', timestring=timestring, filename=filename))

    return render_template('upload.html') 

 

@app.route('/uploads/<timestring>')
def uploaded_files(timestring) : 
    file_url_list = [url_for('uploaded_file',timestring=timestring, filename=aFile).lstrip('/') \
                                         for aFile in getfiles(UPLOAD_FOLDER + '/' + timestring)]
    file_url_list_final = file_url_list

    return render_template('list_files.html',file_url_list=file_url_list_final)

@app.route('/uploads/')
def uploaded_dirs():
    file_url_list = [url_for('uploaded_files', timestring=aDir).lstrip('/') for aDir in getdirs(UPLOAD_FOLDER)]
    file_url_list_final = file_url_list

    return render_template('list_files.html',file_url_list=file_url_list_final)




@app.route('/uploads/<timestring>/<filename>')
def uploaded_file(timestring,filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + '/' + timestring,
                               filename)






if __name__ == '__main__':
    app.host='0.0.0.0'
    app.debug = True
    app.run()
