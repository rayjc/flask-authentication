"""Flask app for Feedbacks"""
from flask import Flask, render_template, request, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db
from sqlalchemy import exc

app = Flask(__name__)
# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
db.create_all()
# debug setup
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "test"
app.debug = True
tool_bar = DebugToolbarExtension(app)
