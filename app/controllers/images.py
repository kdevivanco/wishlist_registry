from app import app
from flask import Flask, render_template
from flask_uploads import UploadSet,IMAGES,configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import SubmitField

app.config['UPLOADED_PHOTOS_DEST'] = 'app/static'

photos = UploadSet('photos',IMAGES)

configure_uploads(app,photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators =[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

    