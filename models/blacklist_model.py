from app import db

class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    student1 = db.Column(db.String(100), nullable=False)
    student2 = db.Column(db.String(100), nullable=False)
    similarity = db.Column(db.Float, nullable=False)

    def __init__(self, student1, student2, similarity):
        self.student1 = student1
        self.student2 = student2
        self.similarity = similarity

    def to_dict(self):
        return {
            "id": self.id,
            "student1": self.student1,
            "student2": self.student2,
            "similarity": self.similarity
        }
