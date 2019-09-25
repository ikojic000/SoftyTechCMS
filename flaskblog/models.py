# PYTHON FILE WITH / FOR DATABASE MODELS

# Imports
from datetime import datetime
from flaskblog import db, login_manager, bcrypt
from flask_user import UserMixin



# Function for fetching user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# DATABASE MODELS
# User table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    email_confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    comments = db.relationship('Comment', backref = 'user', lazy= 'dynamic')
    active = db.Column(db.Boolean(), default=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Post table
class Post(db.Model):
    
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    subtitle = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    headImg = db.Column(db.String(50), nullable=False, default='default.jpg')
    category = db.Column(db.String(30), nullable=False)
    language = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref = 'post', lazy= 'dynamic')
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.language}', '{self.slug}', '{self.date_posted}')"

# Comment table
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Comment('{self.user_id}', '{self.post_id}', '{self.content}')"
"""
print('888')
db.create_all()
print('999')

    # Create 'test@test.com' user with no roles
if not User.query.filter(User.email == 'test@test.com').first():
    user = User(
        username ='test',
        email='test@test.com',
        email_confirmed_at=datetime.utcnow(),
        password = bcrypt.generate_password_hash('123456').decode('utf-8'),
    )
    user.roles.append(Role(name='Reader'))
    db.session.add(user)
    db.session.commit()

    # Create 'admin@admin.com' user with 'Admin' role
if not User.query.filter(User.email == 'admin@admin.com').first():
    user = User(
        username ='admin',
        email='admin@admin.com',
        email_confirmed_at=datetime.utcnow(),
        password= bcrypt.generate_password_hash('123456').decode('utf-8'),
    )
    user.roles.append(Role(name='Admin'))
    db.session.add(user)
    db.session.commit()

print("1010101")
"""