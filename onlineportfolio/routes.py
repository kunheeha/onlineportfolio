import os
import secrets
import random
from flask import render_template, request, url_for, flash, redirect, send_from_directory, jsonify
from flask_login import login_user, logout_user, login_required
from onlineportfolio import app, db, bcrypt
from onlineportfolio.models import Person
from onlineportfolio.forms import LoginForm, AddCVForm, ViewCVForm, AboutForm, AddImageForm


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        me = Person.query.filter_by(email=form.email.data).first()
        if me and bcrypt.check_password_hash(me.password, form.password.data):
            login_user(me)
            return redirect(url_for('admin'))
    return render_template("login.html", form=form)


@app.route('/admin')
@login_required
def admin():
    cvform = AddCVForm()
    aboutform = AboutForm()
    viewcvform = ViewCVForm()
    imageform = AddImageForm()

    return render_template("admin.html", aboutform=aboutform, cvform=cvform, imageform=imageform)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
