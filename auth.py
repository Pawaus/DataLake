from flask import Blueprint, render_template, request, redirect, url_for




auth = Blueprint('auth', __name__)

@auth.route('/login.html',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('base_auth.html')
    elif request.method == 'POST':

        return redirect(url_for('main.index'))

@auth.route('/login_btn')
def login_btn():
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'