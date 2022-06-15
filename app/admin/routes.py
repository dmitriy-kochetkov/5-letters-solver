from app import app, db
from app.admin import bp
from datetime import date, datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.auth.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse


@login_required
@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if current_user.is_admin():
        return render_template('admin/main.html', title='System Administator')
    else:
        return redirect(url_for('main.index'))

