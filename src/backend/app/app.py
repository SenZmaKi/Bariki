""" App main module """
from flask import Flask, redirect, request
from flask import render_template
import db from models.base

app = Flask(__name__)
app.config['SLQALCHEMY_DATABASE_URI'] = "sqlite://bariki.db"

db.init_app(app)

app.route("/")
def index():
    """ Index page """
    return "<h1>Index </h1>"

app.route('/create_user'/)
