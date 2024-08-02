from ..utils import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    is_paid_member = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()    