import os
import secrets
import random
from flask import render_template, request, url_for, flash, redirect, send_from_directory, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from onlineportfolio import app, db, bcrypt, mail
from onlineportfolio.models import Person, User, Skill, SoftwareProject, WebProject
from onlineportfolio.forms import LoginForm, AddCVForm, ViewCVForm, AboutForm, AddImageForm, RequestAddressForm


@app.route('/', methods=['POST', 'GET'])
def index():
    developer = User.query.first()
    profile_photo = url_for('static', filename='images/'+developer.profile_photo)
    me = Person.query.first()
    viewcvform = ViewCVForm()

    if viewcvform.cvsubmit.data and viewcvform.validate():
        cv = me.cv_file
        mydirectory = os.path.join(app.root_path, 'static/cv')
        return send_from_directory(directory=mydirectory, filename=cv)

    return render_template("index.html", viewcvform=viewcvform, me=me, developer=developer, profile_photo=profile_photo)


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


@app.route('/address', methods=['POST', 'GET'])
def address():
    form = RequestAddressForm()
    if form.validate_on_submit():
        visitoremail = form.email.data
        reason = form.reason.data
        toreceive = Message(subject='Address Request', sender=visitoremail,
                            body=f'Sender: {visitoremail}. Reason : {reason}.', recipients=["kunheeha@gmail.com"])
        mail.send(toreceive)
        flash('Your request has been received. Please await an email response', 'success')

    return render_template("foraddress.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        me = Person.query.filter_by(email=form.email.data).first()
        if me and bcrypt.check_password_hash(me.password, form.password.data):
            login_user(me)
            return redirect(url_for('admin'))
    return render_template("login.html", form=form)


def save_cv(form_cv):
    name = 'KunheeHaCV'
    _, f_ext = os.path.splitext(form_cv.filename)
    cv_fn = name + f_ext
    cv_path = os.path.join(app.root_path, 'static/cv', cv_fn)
    form_cv.save(cv_path)

    return cv_fn


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    cvform = AddCVForm()
    aboutform = AboutForm()
    viewcvform = ViewCVForm()
    imageform = AddImageForm()

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

    if aboutform.validate_on_submit():
        current_user.personal_statement = aboutform.personal_statement.data
        db.session.commit()
        flash('Profile Updated', 'success')
    elif request.method == 'GET':
        if current_user.personal_statement:
            aboutform.personal_statement.data = current_user.personal_statement

    return render_template("admin.html", aboutform=aboutform, cvform=cvform, imageform=imageform, viewcvform=viewcvform)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
