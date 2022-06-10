from app import app, db
from app.models import User, Word

USERNAME_1 = 'Dimas'
EMAIL_1 = 'dimas@aziz.com'
PASSWORD_1 = '12345'
USERNAME_2 = 'Boris'
EMAIL_2 = 'boris@aziz.com'
PASSWORD_2 = 'pidor'

def init_db():
    # init user 1
    user1 = User.query.filter_by(username=USERNAME_1).first()
    if not user1:
        user1 = User(username=USERNAME_1, email=EMAIL_1)
    user1.set_password(PASSWORD_1)
    print(user1.password_hash)
    db.session.add(user1)

    #init user 2
    user2= User.query.filter_by(username=USERNAME_2).first()
    if not user2:
        user2 = User(username=USERNAME_2, email=EMAIL_2)
    user2.set_password(PASSWORD_2)
    print(user2.password_hash)
    db.session.add(user2)

    db.session.commit()

if __name__ == '__main__':
    init_db()