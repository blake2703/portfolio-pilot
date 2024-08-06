from ..utils import db


class Stock(db.Model):
    """
    A class that creates the Stock table schema
    """
    __tablename__ = 'stocks'
    
    # define table schema
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    sector = db.Column(db.String(128), nullable=False)
    industry = db.Column(db.String(128), nullable=False)
    
    # foreign key to link to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self) -> str:
        """
        Allow for a printable representation of the Stocks class
        """
        return f"<Ticker {self.ticker}>"
    
    def save(self):
        """
        Save the object to the database table
        """
        db.session.add(self)
        db.session.commit()