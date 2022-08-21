from shop import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180),unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username

class Logs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, unique=False, nullable=False)
    action = db.Column(db.String(200),unique=False, nullable=False)
    time = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now)

#class Orders(db.Model): 
class DiscountGenerator(db.Model):
    dcode = db.Column(db.String(8),unique=True, nullable=False, primary_key=True)
    discount = db.Column(db.Numeric(10,2), nullable=False,unique=False)
    times = db.Column(db.Integer,unique=False, nullable=False)


db.create_all()