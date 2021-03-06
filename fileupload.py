#!/usr/bin/python

from flask import Flask, request, redirect, url_for, render_template, redirect, send_from_directory
import time
from werkzeug.utils import secure_filename
import os
from os import listdir, path
from os.path import isdir, isfile, join
from celery import Celery
from flask_bootstrap import Bootstrap


UPLOAD_FOLDER=os.path.abspath('uploads')


ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


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


def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app


app = create_app() 

app.config.update(
    CELERY_BROKER_URL='redis://guest@localhost:6379',
    CELERY_RESULT_BACKEND='redis://guest@localhost:6379',
    UPLOAD_FOLDER=os.path.abspath('uploads')

    
)

celery = make_celery(app)


@app.route('/', methods=['GET', 'POST']) 
def upload_file() :
    print "MAHESH %s" % app.config['UPLOAD_FOLDER'] 
    if request.method == 'POST' :
        file = request.files['file']
        if file and allowed_file(file.filename) :
            filename=secure_filename(file.filename)
            timestring = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).replace(':','-').replace(' ','-')
            print "MKDIR to %s" % app.config['UPLOAD_FOLDER'] + '/' + timestring

            os.mkdir(app.config['UPLOAD_FOLDER'] + '/' + timestring)
            abs_path = app.config['UPLOAD_FOLDER'] + '/' + timestring
            file.save(os.path.join(abs_path, filename))
            """
            return redirect(url_for('uploaded_file', timestring=timestring, filename=filename))
            """
            from fileupload import long_task
            long_task.delay(30)
            
 
            return redirect(url_for('uploaded_files', timestring=timestring))

    return render_template('upload.html') 

 
@celery.task(name='long_task')

def long_task(delay) :
    print "BEGIN..", time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    time.sleep(delay)
    print "END..", time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return(delay)

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
    return send_from_directory(UPLOAD_FOLDER + '/' + timestring,
                               filename)


@app.route('/boottest/')
def do_boottest() :
    return render_template('test_boot.html') 
    



if __name__ == '__main__':
    app.host='0.0.0.0'
    app.debug = True
    app.run()


"""
Install notes :

pip install celery 
pip install redis
pip install flask
celery -A fileupload.celery  worker --loglevel=info
pip install flask-bootstrap
"""
