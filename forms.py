from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, InputRequired, Length, ValidationError


class AddUserForm(FlaskForm):
    """Form for adding a user."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(message="Please provide a name!"),
            Length(max=20, message="Sorry, this name is too long!")
        ]
    )
    
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Please provide a password!"),
            Length(max=50, message="Sorry, this password is too long!")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            InputRequired(message="Please provide a email!"),
            Length(max=50, message="Sorry, this email is too long!"),
            Email(message="Please enter a valid email address!")
        ]
    )

    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(message="Please provide your name!"),
            Length(max=30, message="Sorry, this name is too long!")
        ]
    )
    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(message="Please provide your name!"),
            Length(max=30, message="Sorry, this name is too long!")
        ]
    )


class LoginUserForm(FlaskForm):
    """Form for adding a user."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(message="Please provide a name!"),
            Length(max=20, message="Sorry, this name is too long!")
        ]
    )
    
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Please provide a password!"),
            Length(max=50, message="Sorry, this password is too long!")
        ]
    )
