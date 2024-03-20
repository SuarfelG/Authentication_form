from flask import Blueprint , render_template ,redirect,url_for,request,flash
from . import db
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
auth=Blueprint("auth",__name__)

@auth.route('/login',methods=['GET','POST'])
def login ():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            try:
                if check_password_hash(user.password, password):
                    flash("Welcome!", category='success')
                    return redirect(url_for('views.home'))
                else:
                    flash("Invalid password.",category="error")
            except Exception as e:
                flash(f"Error verifying password: {e}", category='error')  
            else:
                flash('Password Incorrect', category='error')
        else:
            flash("Email Doesnot Exist",category='error')
    return render_template("login.html")



@auth.route('/signup',methods=['GET','POST'])
def signup ():
    if request.method=="POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exist=User.query.filter_by(email=email).first()

        if email_exist:
            flash('Email Already Exist', category='error')
        elif password1!=password2:
            flash("Passwords don't Match",category='error')
        elif len(email)<5:
            flash("Email Too Short",category='error')
        elif len(username)<6:
            flash('Username Is Too Short',category="error")
        elif len(password1 or password2)<5:
            flash("Password Is Too Short",category="error")
        else:
            new_user=User(email=email,password=generate_password_hash(password1),username=username)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("User successfully Created!", category="success")
            return redirect(url_for('views.home'))


    return render_template("signup.html")

@login_required
@auth.route('/logout' ,methods=['GET','POST'])
def logout ():
    user_id=request.form.get('user_id')
    user=User.query.filter_by(id=user_id).first()  
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User Successfully Deleted",category="success")  
    else:
        flash("User Not Found", category='error')
    return render_template('logout.html')