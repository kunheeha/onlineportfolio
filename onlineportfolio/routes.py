import os
import secrets
import random
from flask import render_template, request, url_for, flash, redirect, send_from_directory, jsonify
from onlineportfolio import app


@app.route('/')
def index():
    return render_template("index.html")
