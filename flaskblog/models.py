from datetime import datetime
from flaskblog import db, login_manager
from flask_user import UserMixin
from passlib.hash import bcrypt


# Function for fetching user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# DATABASE MODELS
# User table
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    password = db.Column(db.String(100), nullable=False)
    roles = db.relationship("Role", secondary="user_roles")
    name = db.Column(db.String(50), nullable=True)
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    active = db.Column(db.Boolean(), default=True)
    request_logs = db.relationship("RequestLog", backref="user", lazy="dynamic")
    error_logs = db.relationship("ErrorLog", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))


# Post table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    headImg = db.Column(db.String(254), nullable=False, default="default.jpg")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref="posts")
    language = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    isPublished = db.Column(db.Boolean(), nullable=False, default=False)
    comments = db.relationship("Comment", backref="post", lazy="dynamic")

    def __repr__(self):
        formatted_date_posted = self.date_posted.strftime("%d-%m-%Y %H:%M:%S")
        return f"Post('{self.title}', '{self.language}', '{self.slug}', '{formatted_date_posted}')"


# Category table
class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Comment table
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __repr__(self):
        return f"Comment('{self.user_id}', '{self.post_id}', '{self.content}')"


# RequestLog Table
class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255))
    methodType = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ErrorLog Table
class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    endpoint = db.Column(db.String(255))
    methodType = db.Column(db.String(10))
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text)


"""
print("------------------DB START------------------")
db.create_all()
print("------------------DB CREATE DONE------------------")

role_reader = Role(name="Reader")
role_admin = Role(name="Admin")
role_superadmin = Role(name="Superadmin")
db.session.add(role_reader)
db.session.add(role_admin)
db.session.add(role_superadmin)
db.session.commit()

print("------------------DB ROLES INSERT DONE------------------")

# Create 'test@test.com' user with no roles
if not User.query.filter(User.email == "test@test.com").first():
    user = User(
        username="test",
        email="test@test.com",
        email_confirmed_at=datetime.utcnow(),
        password=bcrypt.hash("test"),
    )
    user.roles.append(role_reader)
    db.session.add(user)
    db.session.commit()

# Create 'ikojic000@gmail.com' user with 'Admin' role
if not User.query.filter(User.email == "admin@admin.com").first():
    user = User(
        username="ikojic000",
        email="ikojic000@gmail.com",
        email_confirmed_at=datetime.utcnow(),
        password=bcrypt.hash("VreliPenis25"),
    )
    user.roles.append(role_admin)
    user.roles.append(role_superadmin)
    db.session.add(user)
    db.session.commit()

# Admin user
if not User.query.filter(User.email == "admin@admin.com").first():
    user = User(
        username="admin",
        email="admin@admin.com",
        email_confirmed_at=datetime.utcnow(),
        password=bcrypt.hash("admin"),
    )
    user.roles.append(role_admin)
    db.session.add(user)
    db.session.commit()


print("------------------DB USER INSERT DONE------------------")

"""
