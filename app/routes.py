import os
from app import app, db
from app.utils import calculate_variants
from datetime import date, datetime
from flask import render_template, flash, redirect, send_from_directory, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm
from app.models import User, Word, today_added_words
from werkzeug.urls import url_parse


REQUIRED_SYMBOLS = ['.', '^', '!']

STATUS_BAD_REQUEST = 400
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_CONFLICT = 409


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
@login_required
def index():
    today_words = today_added_words()
    variants = calculate_variants(today_words)
    return render_template('index.html', 
                            title='5БУКВ solver', 
                            variants=variants[0:40], 
                            total_variants=len(variants), 
                            today_words=today_words)


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
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/word', methods=['POST',])
def add_word():
    data = request.json
    word_body = data.get('body')
    word_mask = data.get('mask')

    if not word_body or len(word_body) != 5 or not word_body.isalpha():
        return jsonify('wrong data format'), STATUS_BAD_REQUEST

    if not word_mask or len(word_mask) != 5:
        return jsonify('wrong data format'), STATUS_BAD_REQUEST

    for symb in word_mask:
        if symb not in REQUIRED_SYMBOLS:
            return jsonify('wrong data format'), STATUS_BAD_REQUEST

    word = Word(body=word_body.upper(), mask=word_mask, user_id=current_user.id)

    if not word.is_already_exist():
        db.session.add(word)
        db.session.commit()
        return jsonify(word.json_obj())
    else:
        return jsonify('word is already exists'), STATUS_CONFLICT


@login_required
@app.route('/word/<word_id>', methods=['GET',])
def get_word(word_id):
    word = Word.query.get(word_id)
    if not word:
        return jsonify()

    return jsonify(word.json_obj())


@login_required
@app.route('/word/<word_id>', methods=['PUT',])
def update_word(word_id):
    data = request.json
    word_body = data.get('body')
    word_mask = data.get('mask')

    if not word_body or len(word_body) != 5:
        return jsonify('wrong data format'), STATUS_BAD_REQUEST

    if not word_mask or len(word_mask) != 5:
        return jsonify('wrong data format'), STATUS_BAD_REQUEST

    word = Word.query.get(word_id)

    if word:
        word.body = word_body
        word.mask = word_mask
        db.session.commit()
        return jsonify(word.json_obj())
    else:
        return jsonify('word is not exists'), STATUS_NOT_FOUND


@login_required
@app.route('/word/<word_id>', methods=['DELETE',])
def remove_word(word_id):
    word = Word.query.get(word_id)
    if not word:
        return jsonify('not exists'), STATUS_NOT_FOUND

    if word.check_permission(current_user):
        db.session.delete(word)
        db.session.commit()
        return jsonify('done')
    else:
        return jsonify('permission denied'), STATUS_FORBIDDEN


@login_required
@app.route('/actual_words', methods=['GET'])
def actual_words():
    today_words = today_added_words()
    words = []
    for word in today_words:
        words.append(word.json_obj())

    return jsonify(words)


@login_required
@app.route('/calc_variants', methods=['GET'])
def calc_variants():
    today_words = today_added_words()
    variants = calculate_variants(today_words)
    return jsonify({'words': variants[0:40], 'total':len(variants)})
