"""Flask app for Feedbacks"""
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from forms import AddUserForm, LoginUserForm, AddFeedbackForm
from models import connect_db, db, User, Feedback
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
        return redirect(url_for('user_detail_view', username=new_user.username))

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
            return redirect(url_for('user_detail_view', username=username))
        else:
            form.password.errors = ["Username and password do not match!"]
    
    return render_template('login.html', form=form, submit_button="Login")


@app.route('/logout')
def logout_view():
    if 'user' in session:
        del session['user']
        flash('You have been logged out!', 'success')
    return redirect(url_for('login_view'))


@app.route('/secret')
def secret_view():
    if 'user' not in session:
        return redirect(url_for('home_view'))
    
    flash('You made it!', 'success')
    return render_template('base.html')


@app.route('/users/<string:username>')
def user_detail_view(username):
    if session.get('user') == username:
        return render_template(
            'user_detail.html', user=User.query.get_or_404(username)
        )
    else:
        raise Unauthorized("Permission denied.")


# should consider making this a DELETE request and send from AJAX
@app.route('/users/<string:username>/delete', methods=['POST'])
def user_delete_view(username):
    if session.get('user') == username:
        try:
            user = User.query.get_or_404(username)
            db.session.delete(user)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash(f'Failed to remove {username}', 'danger')
            return redirect(url_for('user_detail_view', username=username))
        del session['user']     # log user out
        flash(f'User {username} removed.', 'success')
        return redirect(url_for('home_view'))
    else:
        flash(f'You do not have permission to delete {username}.', 'danger')
        return redirect(url_for('login_view'))


@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def feedback_add_view(username):
    if session.get('user') == username:
        form = AddFeedbackForm()
        
        if form.validate_on_submit():
            title = form.data.get('title')
            content = form.data.get('content')
            try:
                new_feedback = Feedback(title=title, content=content, username=username)
                db.session.add(new_feedback)
                db.session.commit()
            except exc.IntegrityError:
                flash('Failed to create feedback!', 'danger')
                return redirect(url_for('feedback_add_view', username=username))
            flash('Feedback created!', 'success')
            return redirect(url_for('user_detail_view', username=username))
        
        return render_template('feedback_add.html', username=username, form=form, submit_button="Create")
    
    else:
        raise Unauthorized('Permission denied. You can only add feedback under your account.')


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def feedback_edit_view(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username

    if session.get('user') == username:
        form = AddFeedbackForm(obj=feedback)    # populate form
        
        if form.validate_on_submit():
            feedback.title = form.data.get('title')
            feedback.content = form.data.get('content')
            try:
                db.session.add(feedback)
                db.session.commit()
            except exc.IntegrityError:
                flash('Failed to update feedback!', 'danger')
                return redirect(url_for('feedback_edit_view', feedback_id=feedback_id))
            flash('Feedback updated!', 'success')
            return redirect(url_for('user_detail_view', username=username))
        
        return render_template('feedback_edit.html', form=form, submit_button="Update")
    
    else:
        raise Unauthorized('Permission denied. You can only update feedback under your account.')


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def feedback_delete_view(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username

    if session.get('user') == username:
        try:
            db.session.delete(feedback)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash(f'Failed to remove {feedback.title}', 'danger')
        flash(f'Feedback removed.', 'success')
        return redirect(url_for('user_detail_view', username=username))
    else:
        flash(f'You do not have permission to delete this feedback.', 'danger')
        return redirect(url_for('login_view'))
