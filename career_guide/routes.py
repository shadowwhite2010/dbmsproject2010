import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from career_guide import app, db, bcrypt
from werkzeug.utils import secure_filename
from career_guide.models import userr, field, exam, course, college
from flask_login import login_user, current_user, logout_user, login_required
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
    

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
   
    if request.method == "POST":
        
        user = userr.query.filter_by(username = request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            redirect(url_for('home'))
    
    return render_template('sign_in.html')        




        
@app.route("/register", methods=['GET', 'POST'])
def register():
    
    if request.method == "POST":
        
        
        if current_user.is_authenticated:
            current_user.dob = request.form.get("dob")
            
            current_user.gender = request.form.get("gender")
            
            current_user.ambition = request.form.get("ambition")
            
            current_user.qualification = request.form.get("qualification")
            db.session.commit()
            
            flash('You Have Successfully Edited Your Details', 'success')
            return redirect(url_for('register'))
        else:
            username = request.form.get('username')
            user = userr.query.filter_by(username = request.form.get('username')).first()
            if user:
                flash('That username is taken. Please choose a different one.', 'danger')
                return redirect(url_for('register'))
            else:
                dob = request.form.get("dob")
                gender = request.form.get("gender")
                ambition = request.form.get("ambition")
        
                qualification = request.form.get("qualification")
                password = bcrypt.generate_password_hash( request.form.get('password')).decode('utf-8')
                proimg = "download.png"
                
                entry = userr(username=username, password=password, dob=dob, gender=gender, ambition=ambition,  qualification=qualification, proimg=proimg)
                db.session.add(entry)
                db.session.commit()
                flash('You Have Successfully registerd! now please sign-in :)', 'success')
                return redirect(url_for('sign_in'))
    if current_user.is_authenticated:
        proimg = url_for('static', filename='brand/' + current_user.proimg) 
        return render_template('register.html', proimg=proimg) 
    else:          
        return render_template('register.html')       

        
    
@app.route("/delacc")
@login_required
def delacc():
    user = userr.query.filter_by(username=current_user.username).first()
    logout_user()
    db.session.delete(user)
    db.session.commit()
    return render_template('home.html')
   


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.method=="POST":
       
        if 'proimg' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('account'))
        file = request.files['proimg']
        
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            prev_picture = os.path.join(app.root_path, 'static/brand', current_user.proimg)
            if os.path.exists(prev_picture):
                os.remove(prev_picture)


            file.save(os.path.join(app.root_path, 'static/brand', filename))
            current_user.proimg = filename
            db.session.commit()
            return redirect(url_for('account',
                                    filename=filename))

    proimg = url_for('static', filename='brand/' + current_user.proimg)
    return render_template('account.html', proimg=proimg)

@app.route("/carer", methods=['GET', 'POST'])
@login_required
def carer():
    if request.method=="POST":
        if request.form.get("exa")=="Nothing Selected" :
            flash('please select exam to proceed', 'warning')
            return redirect(url_for('account'))
        else:
            val=request.form.get("exa")

            flash(f'you have selcted {val}', 'success')
            return redirect(url_for('cors', val=val))


    examm=exam.query.all()

    user = field.query.filter_by(fieldname=current_user.ambition).first()
    return render_template('carer.html', user=user, examm=examm)


@app.route("/cors/<val>", methods=['GET', 'POST'])
@login_required
def cors(val):
    if request.method=="POST":
        if request.form.get("cr")=="Nothing Selected" :
            flash('please select course to proceed', 'warning')
            return redirect(url_for('cors', val=val))
        else:
            vl=request.form.get("cr")
            flash(f'you have selected {vl}', 'success')
            return redirect(url_for('coll', vl=vl))
    cours=course.query.all()
    return render_template('cors.html', val=val, cours=cours)

@app.route("/coll/<vl>", methods=['GET', 'POST'])
@login_required
def coll(vl):

    colle=college.query.all()
    return render_template('coll.html', vl=vl, colle=colle)    
    

