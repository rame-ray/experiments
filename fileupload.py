#!/usr/bin/python

from flask import Flask, request, redirect, url_for, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask.ext.autoindex import AutoIndex


UPLOAD_FOLDER='/home/mvaidya/misc2/flask_stuff/uploads'
UPLOADS_DEFAULT_DEST=UPLOAD_FOLDER
UPLOADS_DEFAULT_URL='/Dengine'

ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__) 

#AutoIndex(app, browse_root=UPLOAD_FOLDER,add_url_rules=False )

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename) :
    return '.' in filename and \
         filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST']) 
def upload_file() :
    if request.method == 'POST' :
        file = request.files['file']
        if file and allowed_file(file.filename) :
            filename=secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template('upload.html') 

                               

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print "MAHESH %s %s " % (filename, UPLOAD_FOLDER) 
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.host='0.0.0.0'
    app.debug = True
    app.run()
