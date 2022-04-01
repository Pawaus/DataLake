from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('inputEmail')
        passwd = request.form.get('inputPassword')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, passwd):
            flash("Email and/or password is incorrect")
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email = request.form.get('inputEmail')
        passwd = request.form.get('inputPassword')
        login = request.form.get('inputLogin')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already exist')
            return redirect(url_for('auth.register'))
        new_user = User(email=email, name=login, password=generate_password_hash(passwd, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
