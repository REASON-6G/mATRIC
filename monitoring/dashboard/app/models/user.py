from time import time
from datetime import datetime
from flask_login import UserMixin
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid



class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    permissionlevel = db.Column(db.Integer, default=0) #Levels are, User:0, Organization:1, Administrator:2

    def __init__(self, username, password, email, active=False, level=0):
        self.setUUID()
        self.username = username
        self.email = email
        self.setPassword(password)
        self.created_on = datetime.now()
        self.setPermissionLevel(level)
        if level == 2:
            self.active = True
        
    def __repr__(self):
        return self.username
    
    def setUUID(self):
        self.id = str(uuid.uuid4())
        
    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)
    
    def setPermissionLevel(self, level ):
        self.permissionlevel = level

    def to_json(self):        
        return {"username": self.username,
                "email": self.email}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return self.active           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)
        
