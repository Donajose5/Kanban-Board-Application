from .database import db

class User(db.Model):
    __tablename__ = "User"
    UserID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Username = db.Column(db.String, unique=True, nullable=False)
    EmailID = db.Column(db.String)
    Password = db.Column(db.String, nullable=False)

class List(db.Model):
    __tablename__ = "List"
    ListID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey("User.UserID"), unique=True, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Description = db.Column(db.String)
    Created_time = db.Column(db.String, nullable=False)

class Card(db.Model):
    __tablename__ = "Card"
    CardID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ListID = db.Column(db.Integer, db.ForeignKey("List.ListID"), unique=True, nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey("User.UserID"), unique=True, nullable=False)
    Title = db.Column(db.String, nullable=False)
    Content = db.Column(db.String)
    Deadline = db.Column(db.String, nullable=False)
    Complete = db.Column(db.Integer, nullable=False)
    Created_time = db.Column(db.String, nullable=False)
    Last_updated_time = db.Column(db.String, nullable=False)
    Completed_time = db.Column(db.String)