"""Flask app for Feedbacks"""
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from forms import AddUserForm, LoginUserForm
from models import connect_db, db, User
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


@app.route('/')
def home_view():
    return redirect(url_for('register_view'))


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    form = AddUserForm()

    if form.validate_on_submit():
        data = {
            field: value for field, value in form.data.items()
            if field in User.__table__.columns.keys()
        }
        try:
            new_user = User.register(**data)
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            flash("Username/email already exist!", "danger")
            return render_template('register.html', form=form,
                                   submit_button="Register")
        # log user in
        session['user'] = new_user.username
        return redirect(url_for('secret_view'))

    return render_template('register.html', form=form, submit_button="Register")


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.data.get('username')
        password = form.data.get('password')

        user = User.authenticate(username, password)
        if user:
            session["user"] = user.username  # log user in
            return redirect(url_for('secret_view'))
        else:
            form.password.errors = ["Username and password do not match!"]
    
    return render_template('login.html', form=form, submit_button="Login")


@app.route('/secret')
def secret_view():
    flash('You made it!', 'success')
    return render_template('base.html')
