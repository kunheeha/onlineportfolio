from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
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
    cvsubmit = SubmitField('Download CV')


class AboutForm(FlaskForm):
    personal_statement = TextAreaField(
        'Personal Statement', validators=[DataRequired()])
    submit = SubmitField('Save')


class AddImageForm(FlaskForm):
    image_file = FileField('Update Profile Picture', validators=[
                           FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


class RequestAddressForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    reason = StringField('Reason for needing address',
                         validators=[DataRequired()])
    submit = SubmitField('Request Address')


# class ContactForm(FlaskForm):
#     fname = StringField('First Name', validators=[DataRequired()])
#     lname = StringField('Last Name', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     message = TextAreaField('Message', validators=[DataRequired()])
#     submit = SubmitField('Send Message')
