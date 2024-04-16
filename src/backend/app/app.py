""" App main module """
from flask import Flask, redirect, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    """ Index page """
    return "<h1>Index </h1>"

@app.route('/create_user/')
def create_user():
    """ Create user route """
    return "<h1>Create User</h1>"