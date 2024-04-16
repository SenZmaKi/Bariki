""" Module with database models"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """ Base ORM class """
    pass

db = SQLAlchemy(model_class=Base)
