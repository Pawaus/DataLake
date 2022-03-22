from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('inputEmail')
        passwd = request.form.get('inputPassword')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password,passwd):
            return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))


@auth.route('/login_btn')
def login_btn():
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
            return redirect(url_for('auth.register'))
        new_user = User(email=email, name=login, password=generate_password_hash(passwd, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    return 'Logout'
