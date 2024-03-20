from flask import Blueprint,render_template
from flask_login import current_user ,login_required
from .models import User
views=Blueprint("views",__name__)


@views.route('/')
@views.route('/home')
def home ():
    return render_template('home.html')
@views.route('/authenticated_users')
@login_required
def authenticated_users():
        users = User.query.all()
        return render_template('authenticated_users.html', users=users)
    
