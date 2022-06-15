from datetime import datetime, date
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    words = db.relationship('Word', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=user_roles, backref='user',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        for role in self.roles:
            if role.name == 'admin':
                return True
        return False

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    # users = db.relationship('User', secondary=user_roles, backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(64), index=True)
    mask = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Word {}: {}>'.format(self.body, self.mask)

    def is_already_exist(self):
        begin_filter_date = datetime.combine(date.today(), datetime.min.time())
        end_filter_date = datetime.now()

        filters = []
        filters.append(Word.timestamp > begin_filter_date)
        filters.append(Word.timestamp < end_filter_date)
        filters.append(Word.body == self.body)

        result = Word.query.filter(*filters).first()
        if result:
            return True
        return False
    
    def json_obj(self):
        return {
            "id": self.id,
            "body": self.body,
            "mask": self.mask, 
            "datetime": self.timestamp, 
            "author": {
                "id": self.author.id,
                "username": self.author.username
                }
            }
    
    def split_word(self):
        result = []
        for index, letter in enumerate(self.body):
            status = 'excluded'
            if self.mask[index] == '^':
                status = 'included'
            elif self.mask[index] == '!':
                status = 'determined'
            result.append({'symbol': letter, 'status':status})
        return result

    def check_permission(self, user):
        return self.author.id == user.id

def today_added_words():
    begin_filter_date = datetime.combine(date.today(), datetime.min.time())
    end_filter_date = datetime.now()

    filters = []
    filters.append(Word.timestamp > begin_filter_date)
    filters.append(Word.timestamp < end_filter_date)

    return Word.query.filter(*filters).all()
