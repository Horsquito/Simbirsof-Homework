from app import  app, db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, TaskForm
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User, Task

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, body=form.body.data, status=form.status.data)
        user = User.query.filter_by(username=form.performer.data).first()
        if user:
            user.tasks.append(task)
            db.session.add(task)
            db.session.commit()
            flash('Your task is now alive!')
            return redirect(url_for('index'))
        else:
            flash('There is no such developer!')
    tasks = Task.query.all()
    return render_template('index.html', title='Home', tasks=tasks, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse('next_page').netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks = Task.query.filter_by(performer=user).all()
    return render_template('user.html', user=user, tasks=tasks)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', form=form, title='Edit Profile')

@app.route('/explore')
@login_required
def explore():
    tasks = Task.query.order_by(Task.title).all()
    return render_template('/index.html', title='Explore', tasks=tasks)
