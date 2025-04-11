from webapprecon import db
from datetime import datetime

class ScanResults(db.Model):
    '''
    Main Database Table
    '''
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(length=240), nullable=False, unique=True)
    whoisInfo = db.Column(db.Text, nullable=False)
    vulnInfo = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)  

    def __repr__(self) -> str:
        return f"ScanResults: {self.url}"