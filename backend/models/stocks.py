from ..utils import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    sector = db.Column(db.String(128), nullable=False)
    industry = db.Column(db.String(128), nullable=False)
    
    # Foreign key to link to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Ticker {self.ticker}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()