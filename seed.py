from app import app
from models import db, User, Feedback


db.drop_all()
db.create_all()

user1 = User.register("test1", "test", "test1@abc.com", "John", "Doe")
user2 = User.register("test2", "test", "test2@abc.com", "Peter", "Parker")

fb1 = Feedback(
    title="Test Article to U1", content="asl;dfkjal;skjdfl;kajsdl;kfjasl;dkjf",
    username=user1.username
)
fb2 = Feedback(
    title="Second Article to U1", content="...",
    username=user1.username
)
fb3 = Feedback(
    title="Article to U2", content="...",
    username=user2.username
)

db.session.add_all([user1, user2])
db.session.add_all([fb1, fb2, fb3])
db.session.commit()
