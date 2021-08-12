from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
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
                           FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Upload')


class RequestAddressForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    reason = StringField('Reason for needing address',
                         validators=[DataRequired()])
    submit = SubmitField('Request Address')

class SkillForm(FlaskForm):
    skill_name = StringField('Skill Name', validators=[DataRequired()])
    proficiency_level = IntegerField('Proficiency Level', validators=[DataRequired()])
    submit = SubmitField('Save')

class APIProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    source_code = StringField('Source Code', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    user_guide = FileField('Add User Guide', validators=[FileAllowed(['doc', 'docx', 'pdf'])])
    upcoming_functionality = TextAreaField('Upcoming Functionality')
    submit = SubmitField('Save')

class SoftwareProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    source_code = StringField('Source Code', validators=[DataRequired()])
    windows_file = FileField('Add Windows exe', validators=[FileAllowed(['zip', 'exe'])])
    macos_file = FileField('Add MacOS app', validators=[FileAllowed(['app', 'zip'])])
    linux_file = FileField('Add User Guide', validators=[FileAllowed(['zip'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    installation_guide = FileField('Add Installation Guide', validators=[FileAllowed(['doc', 'docx', 'pdf'])])
    user_guide = FileField('Add User Guide', validators=[FileAllowed(['doc', 'docx', 'pdf'])])
    upcoming_functionality = TextAreaField('Upcoming Functionality')
    submit = SubmitField('Save')

class WebProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    source_code = StringField('Source Code', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    user_guide = FileField('Add User Guide', validators=[FileAllowed(['doc', 'docx', 'pdf'])])
    upcoming_functionality = TextAreaField('Upcoming Functionality')
    submit = SubmitField('Save')   
