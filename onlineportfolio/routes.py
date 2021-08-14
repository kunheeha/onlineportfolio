import os
import secrets
import random
from flask import render_template, request, url_for, flash, redirect, send_from_directory, jsonify, send_file
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
        cv = f'static/cv/{developer.cv_file}'
        mydirectory = os.path.join(app.root_path, cv)
        return send_file(mydirectory, as_attachment=True)

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


@app.route('/download/<int:project_id>/<filetype>')
def downloadfile(project_id, filetype):
    project = SoftwareProject.query.get(project_id)
    if filetype == 'windows':
        windowsfile = f'static/{project.name}/{project.windows_file}'
        mydirectory = os.path.join(app.root_path, windowsfile)
        return send_file(mydirectory, as_attachment=True)
    elif filetype == 'macos':
        macosfile = f'static/{project.name}/{project.macos_file}'
        mydirectory = os.path.join(app.root_path, macosfile)
        return send_file(mydirectory, as_attachment=True)
    elif filetype == 'linux':
        linuxfile = f'static/{project.name}/{project.linux_file}'
        mydirectory = os.path.join(app.root_path, linuxfile)
        return send_file(mydirectory, as_attachment=True)

@app.route('/software/<int:project_id>')
def downloads(project_id):
    project = SoftwareProject.query.get_or_404(project_id)
    return render_template('downloads.html', project=project)

@app.route('/APIProject/<int:project_id>/info')
def apiprojectinfo(project_id):
    project = APIProject.query.get_or_404(project_id)
    return render_template('web_info.html', project=project)

@app.route('/SoftwareProject/<int:project_id>/info')
def softwareprojectinfo(project_id):
    project = SoftwareProject.query.get_or_404(project_id)
    return render_template('software_info.html', project=project)

@app.route('/WebProject/<int:project_id>/info')
def webprojectinfo(project_id):
    project = WebProject.query.get_or_404(project_id)
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

    return profile_photo_fn

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    skills = Skill.query.all()
    apiprojects = APIProject.query.all()
    webprojects = WebProject.query.all()
    softwareprojects = SoftwareProject.query.all()

    cvform = AddCVForm()
    aboutform = AboutForm()
    imageform = AddImageForm()
    skillform = SkillForm()

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

    return render_template("admin.html", aboutform=aboutform, cvform=cvform, imageform=imageform, skills=skills, skillform=skillform, webprojects=webprojects, apiprojects=apiprojects, softwareprojects=softwareprojects)

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

def save_userguide(projectname, form_user_guide):
    name = f'{projectname}_userguide'
    _, f_ext = os.path.splitext(form_user_guide.filename)
    userguide_fn = name + f_ext
    userguide_path = os.path.join(app.root_path, f'static/{projectname}', userguide_fn)
    try:
        form_user_guide.save(userguide_path)
    except:
        path = os.path.join(app.root_path, 'static')
        os.mkdir(f'{path}/{projectname}')
        form_user_guide.save(userguide_path)

    return userguide_fn

def save_installguide(projectname, form_install_guide):
    name = f'{projectname}_installguide'
    _, f_ext = os.path.splitext(form_install_guide.filename)
    installguide_fn = name + f_ext
    installguide_path = os.path.join(app.root_path, f'static/{projectname}', installguide_fn)
    try:
        form_install_guide.save(installguide_path)
    except:
        path = os.path.join(app.root_path, 'static')
        os.mkdir(f'{path}/{projectname}')
        form_install_guide.save(installguide_path)

    return installguide_fn

def save_windows(projectname, form_windows_file):
    windows_fn = form_windows_file.filename
    path = os.path.join(app.root_path, f'static/{projectname}', windows_fn)
    try:
        form_windows_file.save(path)
    except:
        newpath = os.path.join(app.root_path, 'static')
        os.mkdir(f'{newpath}/{projectname}')
        form_windows_file.save(path)

    return windows_fn

def save_macos(projectname, form_macos_file):
    macos_fn = form_macos_file.filename
    path = os.path.join(app.root_path, f'static/{projectname}', macos_fn)
    try:
        form_macos_file.save(path)
    except:
        newpath = os.path.join(app.root_path, 'static')
        os.mkdir(f'{newpath}/{projectname}')
        form_macos_file.save(path)

    return macos_fn

def save_linux(projectname, form_linux_file):
    linux_fn = form_linux_file.filename
    path = os.path.join(app.root_path, f'static/{projectname}', linux_fn)
    try:
        form_linux_file.save(path)
    except:
        newpath = os.path.join(app.root_path, 'static')
        os.mkdir(f'{newpath}/{projectname}')
        form_linux_file.save(path)

    return linux_fn

@app.route('/APIProject/add', methods=['GET', 'POST'])
@login_required
def apiprojectnew():
    form = APIProjectForm()
    if form.validate_on_submit():
        project = APIProject(name=form.name.data, source_code=form.source_code.data, link=form.link.data, description=form.description.data)
        if form.user_guide.data:
            userguide = save_userguide(form.name.data, form.user_guide.data)
            project.user_guide = userguide 
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.add(project)
        db.session.commit()
        newpath = os.path.join(app.root_path, 'static')
        os.mkdir(f'{newpath}/{project.name}')
        return redirect(url_for('admin'))
    return render_template('web_project_new.html', form=form)

@app.route('/SoftwareProject/add', methods=['GET', 'POST'])
@login_required
def softwareprojectnew():
    form = SoftwareProjectForm()
    if form.validate_on_submit():
        project = SoftwareProject(name=form.name.data, source_code=form.source_code.data, description=form.description.data)
        if form.windows_file.data:
            windowsfile = save_windows(form.name.data, form.windows_file.data)
            project.windows_file = windowsfile
        if form.macos_file.data:
            macosfile = save_macos(form.name.data, form.macos_file.data)
            project.macos_file = macosfile
        if form.linux_file.data:
            linuxfile = save_linux(form.name.data, form.linux_file.data)
            project.linux_file = linuxfile
        if form.installation_guide.data:
            installguide = save_installguide(form.name.data, form.installation_guide.data)
            project.installation_guide = installguide
        if form.user_guide.data:
            userguide = save_userguide(form.name.data, form.user_guide.data)
            project.user_guide = userguide 
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.add(project)
        db.session.commit()
        newpath = os.path.join(app.root_path, 'static')
        os.mkdir(f'{newpath}/{project.name}')
        return redirect(url_for('admin'))
    return render_template('software_project_new.html', form=form)

@app.route('/WebProject/add', methods=['GET', 'POST'])
@login_required
def webprojectnew():
    form = WebProjectForm()
    if form.validate_on_submit():
        project = WebProject(name=form.name.data, source_code=form.source_code.data, link=form.link.data, description=form.description.data)
        if form.user_guide.data:
            userguide = save_userguide(form.name.data, form.user_guide.data)
            project.user_guide = userguide 
        if form.upcoming_functionality.data:
            project.upcoming_functionality = form.upcoming_functionality.data
        db.session.add(project)
        db.session.commit()
        newpath = os.path.join(app.root_path, 'static')
        os.mkdir(f'{newpath}/{project.name}')
        return redirect(url_for('admin'))
    return render_template('web_project_new.html', form=form)

@app.route('/APIProject/<int:project_id>/edit', methods=['GET', 'POST'])
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
            if not project.user_guide:
                userguide = save_userguide(form.name.data, form.user_guide.data)
                project.user_guide = userguide 
            elif project.user_guide:
                user_guide_filename = project.user_guide 
                path = os.path.join(app.root_path, f'static/{project.name}', user_guide_filename)
                os.remove(path)
                userguide = save_userguide(form.name.data, form.user_guide.data)
                project.user_guide = userguide 
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
    return render_template('web_project_edit.html', form=form, project=project)

@app.route('/SoftwareProject/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def softwareprojectedit(project_id):
    project = SoftwareProject.query.get_or_404(project_id)
    form = SoftwareProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.source_code = form.source_code.data
        project.description = form.description.data

        if form.windows_file.data:
            if not project.windows_file:
                windowsfile = save_windows(form.name.data, form.windows_file.data)
                project.windows_file = windowsfile
            elif project.windows_file:
                windows_file_name = project.windows_file
                path = os.path.join(app.root_path, f'static/{project.name}', windows_file_name)
                os.remove(path)
                windowsfile = save_windows(form.name.data, form.windows_file.data)
                project.windows_file = windowsfile

        if form.macos_file.data:
            if not project.macos_file:
                macosfile = save_macos(form.name.data, form.macos_file.data)
                project.macos_file = macosfile
            elif project.macos_file:
                macos_file_name = project.macos_file
                path = os.path.join(app.root_path, f'static/{project.name}', macos_file_name)
                os.remove(path)
                macosfile = save_macos(form.name.data, form.macos_file.data)
                project.macos_file = macosfile

        if form.linux_file.data:
            if not project.linux_file:
                linuxfile = save_linux(form.name.data, form.linux_file.data)
                project.linux_file = linuxfile
            elif project.linux_file:
                linux_file_name = project.linux_file
                path = os.path.join(app.root_path, f'static/{project.name}', linux_file_name)
                os.remove(path)
                linuxfile = save_linux(form.name.data, form.linux_file.data)
                project.linux_file = linuxfile

        if form.user_guide.data:
            if not project.user_guide:
                userguide = save_userguide(form.name.data, form.user_guide.data)
                project.user_guide = userguide 
            elif project.user_guide:
                user_guide_filename = project.user_guide 
                path = os.path.join(app.root_path, f'static/{project.name}', user_guide_filename)
                os.remove(path)
                userguide = save_userguide(form.name.data, form.user_guide.data)
                project.user_guide = userguide 

        if form.installation_guide.data:
            if not project.installation_guide:
                installguide = save_installguide(form.name.data, form.installation_guide.data)
                project.installation_guide = installguide
            elif project.installation_guide:
                installation_guide_filename = project.installation_guide
                path = os.path.join(app.root_path, f'static/{project.name}', installation_guide_filename)
                os.remove(path)
                installguide = save_installguide(form.name.data, form.installation_guide.data)
                project.installation_guide = installguide

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

@app.route('/WebProject/<int:project_id>/edit', methods=['GET', 'POST'])
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
            if not project.user_guide:
                userguide = save_userguide(form.name.data, form.user_guide.data)
                project.user_guide = userguide 
            elif project.user_guide:
                user_guide_filename = project.user_guide 
                path = os.path.join(app.root_path, f'static/{project.name}', user_guide_filename)
                os.remove(path)
                userguide = save_userguide(form.name.data, form.user_guide.data)
                project.user_guide = userguide 
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
    return render_template('web_project_edit.html', form=form, project=project)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
