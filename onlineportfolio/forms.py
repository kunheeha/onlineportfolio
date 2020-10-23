from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddCVForm(FlaskForm):
    cv_file = FileField('Add CV', validators=[
                        FileAllowed(['doc', 'docx', 'pdf'])])
    submit = SubmitField('Upload')


class ViewCVForm(FlaskForm):
    submit = SubmitField('Download CV')


class AboutForm(FlaskForm):
    personal_statement = StringField(
        'Personal Statement', validators=[DataRequired()])
    submit = SubmitField('Save')


class AddImageForm(FlaskForm):
    image_file = FileField('Update Profile Picture', validators=[
                           FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')
