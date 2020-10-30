import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        
        img = cv2.imread(filename) 

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

        stop_data = cv2.CascadeClassifier('stop_data.xml') 
        
        found = stop_data.detectMultiScale(img_gray,  
                                        minSize =(20, 20)) 
        
        # Don't do anything if there's  
        # no sign 
        amount_found = len(found) 
        
        if amount_found != 0: 
            
            
            for (x, y, width, height) in found: 
                
                # every recognized sign 
                cv2.rectangle(img_rgb, (x, y),  
                            (x + height, y + width),  
                            (0, 255, 0), 5)     
        os.chdir('static/uploads')
        img1 = Image.fromarray(img_rgb, 'RGB')
        img1.save('test.jpg')
        filename = 'test.jpg'
        print(type(filename))


        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()