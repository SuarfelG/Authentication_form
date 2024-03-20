from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id=db.Column( db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)  
    email = db.Column(db.String(100), nullable=False , unique=True) 
    password = db.Column(db.String(100), nullable=False ) 
    datetime =db.Column(db.DateTime(timezone=True),server_default=func.now())
    
