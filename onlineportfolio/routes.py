import os
import secrets
import random
from flask import render_template, request, url_for, flash, redirect, send_from_directory, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from onlineportfolio import app, db, bcrypt, mail
from onlineportfolio.models import Person, User, Skill, SoftwareProject, WebProject, APIProject
from onlineportfolio.forms import LoginForm, AddCVForm, ViewCVForm, AboutForm, AddImageForm, RequestAddressForm, SkillForm, APIProjectForm, SoftwareProjectForm, WebProjectForm


@app.route('/', methods=['POST', 'GET'])
def index():
    developer = User.query.first()
    profile_photo = url_for('static', filename='images/'+developer.profile_photo)
    viewcvform = ViewCVForm()
    skills = Skill.query.all()
    softwareprojects = SoftwareProject.query.all()
    webprojects = WebProject.query.all()
    apiprojects = APIProject.query.all()


    if viewcvform.cvsubmit.data and viewcvform.validate():
        cv = developer.cv_file
        mydirectory = os.path.join(app.root_path, 'static/cv')
        return send_from_directory(directory=mydirectory, filename=cv)

    return render_template("index.html", viewcvform=viewcvform, developer=developer, profile_photo=profile_photo, skills=skills, softwareprojects=softwareprojects, webprojects=webprojects, apiprojects=apiprojects)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        senderName = fname + ' ' + lname
        senderEmail = request.form['email']
        sentmsg = request.form['message']
        toreceive = Message(subject='Portfolio Message', sender='kunheeha@gmail.com',
                            recipients=["kunheeha@gmail.com"])
        tosend = Message(subject='Message Received', sender='kunheeha@gmail.com',
                         recipients=[senderEmail])
        toreceive.html = render_template(
            'message.html', senderName=senderName, senderEmail=senderEmail, sentmsg=sentmsg)
        tosend.html = render_template(
            'autorespond.html', senderName=senderName)

        try:
            mail.send(toreceive)
            mail.send(tosend)
            return jsonify(status=True)

        except:
            return jsonify(status=False)

@app.route('/APIProject/<int:project_id>/info')
def apiprojectinfo(project_id):
    project = APIProject.query.get(project_id)
    return render_template('web_info.html', project=project)

@app.route('/SoftwareProject/<int:project_id>/info')
def softwareprojectinfo(project_id):
    project = SoftwareProject.query.get(project_id)
    return render_template('software_info.html', project=project)

@app.route('/WebProject/<int:project_id>/info')
def webprojectinfo(project_id):
    project = WebProject.query.get(project_id)
    return render_template('web_info.html', project=project)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        developer = User.query.first()
        if bcrypt.check_password_hash(developer.password, form.password.data):
            login_user(developer)
            return redirect(url_for('admin'))
    return render_template("login.html", form=form)


def save_cv(form_cv):
    name = 'KunheeHaCV'
    _, f_ext = os.path.splitext(form_cv.filename)
    cv_fn = name + f_ext
    cv_path = os.path.join(app.root_path, 'static/cv', cv_fn)
    form_cv.save(cv_path)

    return cv_fn

def save_profile_photo(form_profile_photo):
    name = 'ProfilePhoto'
    _, f_ext = os.path.splitext(form_profile_photo.filename)
    profile_photo_fn = name + f_ext
    profile_photo_path = os.path.join(app.root_path, 'static/images', profile_photo_fn)
    form_profile_photo.save(profile_photo_path)

    return cv_fn

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    skills = Skill.query.all()

    cvform = AddCVForm()
    aboutform = AboutForm()
    viewcvform = ViewCVForm()
    imageform = AddImageForm()
    skillform = SkillForm()

    if viewcvform.cvsubmit.data and viewcvform.validate():
        me = Person.query.first()
        cv = me.cv_file
        mydirectory = os.path.join(app.root_path, 'static/cv')
        return send_from_directory(directory=mydirectory, filename=cv)

    if cvform.validate_on_submit():
        if not current_user.cv_file:
            if cvform.cv_file.data:
                cv = save_cv(cvform.cv_file.data)
                current_user.cv_file = cv
                db.session.commit()
                flash('Your CV has been uploaded', 'success')
        elif current_user.cv_file:
            if cvform.cv_file.data:
                cvfilename = current_user.cv_file
                path = os.path.join(app.root_path, 'static/cv', cvfilename)
                os.remove(path)
                cv = save_cv(cvform.cv_file.data)
                current_user.cv_file = cv
                db.session.commit()
                flash('Your CV has been updated', 'success')

    if imageform.validate_on_submit():
        if not current_user.profile_photo:
            if imageform.image_file.data:
                profilephoto = save_profile_photo(imageform.image_file.data)
                current_user.profile_photo = profilephoto
                db.session.commit()
                flash('Your Profile Photo has been uploaded', 'success')
        elif current_user.profile_photo:
            if imageform.image_file.data:
                profilephotofilename = current_user.profile_photo
                path = os.path.join(app.root_path, 'static/images', profilephotofilename)
                os.remove(path)
                profilephoto = save_profile_photo(imageform.image_file.data)
                current_user.profile_photo = profilephoto
                db.session.commit()
                flash('Your Profile Photo has been updated', 'success')

    if aboutform.validate_on_submit():
        current_user.personal_statement = aboutform.personal_statement.data
        db.session.commit()
        flash('Profile Updated', 'success')
    elif request.method == 'GET':
        if current_user.personal_statement:
            aboutform.personal_statement.data = current_user.personal_statement

    if skillform.validate_on_submit():
        newskill = Skill(skill_name=skillform.skill_name.data, proficiency_level=skillform.proficiency_level.data)
        db.session.add(newskill)
        db.session.commit()
        flash('New Skill Added', 'success')

    return render_template("admin_test.html", aboutform=aboutform, cvform=cvform, imageform=imageform, viewcvform=viewcvform, skills=skills, skillform=skillform)

@app.route('/skill/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def skilledit(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    skillform = SkillForm()
    if skillform.validate_on_submit():
        skill.skill_name = skillform.skill_name.data
        skill.proficiency_level = skillform.proficiency_level.data
        db.session.commit()
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        skillform.skill_name.data = skill.skill_name
        skillform.proficiency_level.data = skill.proficiency_level
    return render_template("skilledit.html", skillform=skillform)
    
@app.route('/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
def skilldelete(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/APIProject/add', methods=['GET', 'POST'])
@login_required
def apiprojectnew():
    form = APIProjectForm()
    if form.validate_on_submit():
        project = APIProject(name=form.name.data, source_code=form.source_code.data, link=form.link.data, description=form.description.data)
        if form.user_guide.data:
            project.user_guide = form.user_guide.data
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('web_project_new.html', form=form)

@app.route('/SoftwareProject/add', methods=['GET', 'POST'])
@login_required
def softwareprojectnew():
    form = SoftwareProjectForm()
    if form.validate_on_submit():
        project = SoftwareProject(name=form.name.data, source_code=form.source_code.data, description=form.description.data)
        if form.windows_file.data:
            project.windows_file = form.windows_file.data
        if form.macos_file.data:
            project.macos_file = form.macos_file.data
        if form.linux_file.data:
            project.linux_file = form.linux_file.data
        if form.installation_guide.data:
            project.installation_guide = form.installation_guide.data
        if form.user_guide.data:
            project.user_guide = form.user_guide.data
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('software_project_new.html', form=form)

@app.route('/WebProject/add', methods=['GET', 'POST'])
@login_required
def webprojectnew():
    form = WebProjectForm()
    if form.validate_on_submit():
        project = WebProject(name=form.name.data, source_code=form.source_code.data, link=form.link.data, description=form.description.data)
        if form.user_guide.data:
            project.user_guide = form.user_guide.data
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('web_project_new.html', form=form)

@app.route('/APIProject/<int:project_id>/edit')
@login_required
def apiprojectedit(project_id):
    project = APIProject.query.get_or_404(project_id)
    form = APIProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.source_code = form.source_code.data
        project.link = form.link.data
        project.description = form.description.data
        if form.user_guide.data:
            project.user_guide = form.user_guide.data
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.commit()
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.name.data = project.name
        form.source_code.data = project.source_code
        form.link.data = project.link
        form.description.data = project.description
        form.upcoming_functionality.data = project.upcoming_functionality
    return render_template('web_project_new.html', form=form)

@app.route('/SoftwareProject/<int:project_id>/edit')
@login_required
def softwareprojectedit(project_id):
    project = SoftwareProject.query.get_or_404(project_id)
    form = SoftwareProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.source_code = form.source_code.data
        project.description = form.description.data
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.commit()
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.name.data = project.name
        form.source_code.data = project.source_code
        form.description.data = project.description
        form.upcoming_functionality.data = project.upcoming_functionality
    return render_template('software_project_new.html', form=form)

@app.route('/WebProject/<int:project_id>/edit')
@login_required
def webprojectedit(project_id):
    project = WebProject.query.get_or_404(project_id)
    form = WebProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.source_code = form.source_code.data
        project.link = form.link.data
        project.description = form.description.data
        if form.user_guide.data:
            project.user_guide = form.user_guide.data
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.commit()
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.name.data = project.name
        form.source_code.data = project.source_code
        form.link.data = project.link
        form.description.data = project.description
        form.upcoming_functionality.data = project.upcoming_functionality
    return render_template('web_project_new.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
