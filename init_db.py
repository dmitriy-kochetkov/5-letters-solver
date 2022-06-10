from app import app, db
from app.models import User, Word

def init_db():
    user1 = User(username='Boris', email='boris@aziz.com')
    user1.set_password('pidor')
    db.session.add(user1)

    user2 = User(username='Dimas', email='dimas@aziz.com')
    user1.set_password('12345')
    db.session.add(user2)

    db.session.commit()

if __name__ == '__main__':
    init_db()