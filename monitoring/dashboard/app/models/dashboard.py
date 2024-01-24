from app.extensions import db

class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(100))
   
    def __init__(self, url):
        self.url = url
        
    def __repr__(self):
        return self.url
    
    def to_json(self):        
        return {"id": self.id, "url": self.url}
        
    def setURL(self,url):
        self.url = url
