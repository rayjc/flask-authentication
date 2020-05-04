from app import app
from models import db, User


db.drop_all()
db.create_all()

user1 = User.register("test1", "test", "test1@abc.com", "John", "Doe")
user2 = User.register("test2", "testing", "test2@abc.com", "Peter", "Parker")

db.session.add_all([user1, user2])
db.session.commit()
import pdb; pdb.set_trace()