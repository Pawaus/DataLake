from flask import Flask, flash, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from auth import auth as auth_blueprint
from main import main as main_blueprint
import back
import db_sqllite

backend = back.back()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    db.create_all(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    return app
