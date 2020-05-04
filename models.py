"""Models for Feedback app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    bcrypt = Bcrypt()

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = cls.bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(
            username=username, password=hashed_utf8, email=email,
            first_name=first_name, last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, pwd):
        """
        Validate that user exists & password is correct.
        Return user if valid; else return None.
        """

        user = cls.query.filter_by(username=username).first()

        if user and cls.bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return None

    def __repr__(self):
        return (f"<User: username='{self.username}' "
                f"email='{self.email}' "
                f"first_name={self.first_name} "
                f"last_name={self.last_name}>")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
