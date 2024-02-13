from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash , request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm , LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)



# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# TODO: Create a User table for all your registered users. 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100),unique = True)

with app.app_context():
    db.create_all()


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register',methods = ["GET","POST"])
def register():
    register = RegisterForm()
    user = User()
    users = db.session.execute(db.select(User)).scalars().all()
    emails = []
    for user in users:
        emails.append(user.email)
    if request.method == "POST":
        if register.data["email"] in emails:
            flash("You already signed up! log in instead")
            return redirect('login')
        elif register.validate_on_submit():
            new_user = User()
            new_user.name = register.data["name"]
            new_user.email = register.data["email"]
            password = register.data["password"]
            new_user.password = generate_password_hash( password, method='pbkdf2:sha256', salt_length=16)
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("register.html",form = register , logged_in = current_user.is_authenticated)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login',methods = ["GET","POST"])
def login():
    login = LoginForm()
    if request.method == "POST":
        email = login.data["email"]
        password = login.data["password"]
        user =db.session.execute(db.Select(User).where(User.email == email)).scalar()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Wrong Password")
                return redirect('login')
        else:
            flash("This Email doesn't exist")
            return redirect('login')

    return render_template("login.html",form = login, logged_in = current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts , logged_in = current_user.is_authenticated,user = current_user)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post, logged_in = current_user.is_authenticated,user = current_user)


# TODO: Use a decorator so only an admin user can create a new post
# @admin_only
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in = current_user.is_authenticated)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, logged_in = current_user.is_authenticated)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html", logged_in = current_user.is_authenticated)


@app.route("/contact")
def contact():
    return render_template("contact.html", logged_in = current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
