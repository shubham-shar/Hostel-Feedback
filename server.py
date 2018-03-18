from flask import Flask, render_template, url_for, request, redirect, flash
from flask import session as term
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from database import Base, OtherFeedback, FacilitiesFeedback, Water, Mess, staff, Students, Admins


engine = create_engine('sqlite:///feedback.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/feedback')
def Feedback():
    if 'type' in term and term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('AdminPage'))
    return render_template('feedback.html')

@app.route('/admin')
def AdminPage():
    if 'logged_in' not in term:
        flash("Not Logged in")
        return redirect(url_for('Login'))
    if 'type' in term and not term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('Feedback'))
    return render_template('admin/index.html')

@app.route('/signup', methods = ['GET', 'POST'])
def Signup():
    if 'logged_in' in term:
        return redirect(url_for('Feedback'))
    error = None
    if request.method == 'POST':
        password = request.form['Password']
        repass = request.form['Repass']
        email = request.form['Email']
        adminkey = request.form['key']
        if adminkey == "Adminkey":
            if session.query(Admins).filter_by(email = email).first() is not None:
                error = "Admin exists"
                return render_template('signup.html', error = error)

            if password == repass:
                admin = Admins(name = request.form['Name'], email = email)
                admin.hash_password(password)
                session.add(admin)
                session.commit()
                user = session.query(Admins).filter_by(email = email).first()
                term['logged_in'] = True
                term['user_id'] = user.id
                term['email'] = email
                term['type'] = "admin"
                flash("Welcome Admin")
                return redirect(url_for('AdminPage'))
        else:
            if session.query(Students).filter_by(email = email).first() is not None:
                error = "Student exists"
                return render_template('signup.html', error = error)

            if password == repass:
                student = Students(name = request.form['Name'], email = email)
                student.hash_password(password)
                session.add(student)
                session.commit()
                user = session.query(Students).filter_by(email = email).first()
                term['logged_in'] = True
                term['user_id'] = user.id
                term['email'] = email
                term['type'] = "student"
                flash("Welcome!")
                return redirect(url_for('Feedback'))
            else:
                error="password and retyped password not match"
                return render_template('signup.html', error = error)
    else:
        return render_template('signup.html', error = error)

@app.route('/login', methods=['GET', 'POST'])
def Login():
    error = None
    if 'logged_in' in term:
        return redirect(url_for('Feedback'))
    if request.method == 'POST':
        usertype = request.form['user-type']
        if usertype == "Student":
            user = session.query(Students).filter_by(email = request.form['Email']).first()
            if not user:
                error = "Signup First or check your email again"
                return render_template('login.html', error=error)
            elif not user.verify_password(request.form['Password']):
                error = "Wrong Password"
                return render_template('login.html', error=error)
            else:
                term['logged_in'] = True
                term['user_id'] = user.id
                term['email'] = user.email
                term['type'] = "student"
                flash("Welcome back!")
                return redirect(url_for('Feedback'))
        else:
            user = session.query(Admins).filter_by(email = request.form['Email']).first()
            if not user:
                error = "Signup First or check your email again"
                return render_template('login.html', error=error)
            elif not user.verify_password(request.form['Password']):
                error = "Wrong Password"
                return render_template('login.html', error=error)
            else:
                term['logged_in'] = True
                term['user_id'] = user.id
                term['email'] = user.email
                term['type'] = "admin"
                flash("Welcome back admin!")
                return redirect(url_for('AdminPage'))
    else:
        return render_template('login.html', error=error)

@app.route('/logout')
def Logout():
    del term['logged_in']
    del term['user_id']
    del term['email']
    del term['type']
    flash("logged out")
    return redirect(url_for('Feedback'))

@app.route('/feedback/staff', methods = ['GET', 'POST'])
def StaffFeedback():
    if 'logged_in' not in term:
        flash("Not Logged in")
        return redirect(url_for('Login'))
    if 'type' in term and term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('AdminPage'))
    if request.method == 'POST':
        newFeedback = staff(Caretaker = request.form['Caretaker'],
                            Wardens = request.form['Wardens'],
                            Principal = request.form['Principal'],
                            Behaviour = request.form['Behaviour'],
                            Problems = request.form['Problems'],
                            Rating = request.form['Rating'])
        session.add(newFeedback)
        session.commit()
        flash("You Submitted a feedback")
        return render_template('staff.html')
    else:
        return render_template('staff.html')

@app.route('/feedback/water', methods=['GET', 'POST'])
def WaterFeedback():
    if 'logged_in' not in term:
        flash("Not Logged in")
        return redirect(url_for('Login'))
    if 'type' in term and term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('AdminPage'))
    if request.method == 'POST':
        newFeedback = Water(Water = request.form['Water'],
                            Quality = request.form['Quality'],
                            Quantity = request.form['Quantity'],
                            Variety = request.form['Variety'],
                            Cost = request.form['Cost'])
        session.add(newFeedback)
        session.commit()
        flash("You Submitted a feedback")
        return render_template('water.html')
    else:
        return render_template('water.html')

@app.route('/feedback/mess', methods=['GET', 'POST'])
def MessFeedback():
    if 'logged_in' not in term:
        flash("Not Logged in")
        return redirect(url_for('Login'))
    if 'type' in term and term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('AdminPage'))
    if request.method == 'POST':
        newFeedback = Mess(Morning = request.form['Morning'],
                           Afternoon = request.form['Afternoon'],
                           Evening = request.form['Evening'],
                           Dinner = request.form['Dinner'],
                           Availability = request.form['Availability'],
                           Quality = request.form['Quality'],
                           Behaviour = request.form['Behaviour'])
        session.add(newFeedback)
        session.commit()
        flash("You Submitted a feedback")
        return render_template('mess.html')
    else:
        return render_template('mess.html')

@app.route('/feedback/facilities', methods = ['GET','POST'])
def Facilities():
    if 'logged_in' not in term:
        flash("Not Logged in")
        return redirect(url_for('Login'))
    if 'type' in term and term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('AdminPage'))
    if request.method == 'POST':
        newFeedback = FacilitiesFeedback(Room = request.form['Room'],
                                        Corridors = request.form['Corridors'],
                                        Toilets = request.form['Toilets'],
                                        Croom = request.form['Croom'],
                                        Lawns = request.form['Lawns'])
        session.add(newFeedback)
        session.commit()
        flash("You Submitted a feedback")
        return render_template('facilities.html')
    else:
        return render_template('facilities.html')

@app.route('/feedback/others', methods = ['GET', 'POST'])
def Others():
    if 'logged_in' not in term:
        flash("Not Logged in")
        return redirect(url_for('Login'))
    if 'type' in term and term['type'] == "admin":
        flash("Not Authorised to access this page.")
        return redirect(url_for('AdminPage'))
    if request.method == 'POST':
        newFeedback = OtherFeedback(Availability = request.form['Availability'],
                                    Services = request.form['Services'])
        session.add(newFeedback)
        session.commit()
        flash("You Submitted a feedback")
        return render_template('others.html')
    else:
        return render_template('others.html')

@app.route('/admin/mess')
def AdminMess():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if 'type' in term and not term['type'] == "admin":
        return redirect(url_for('Login'))
    Morning = session.query(Mess.Morning).all()
    Afternoon = session.query(Mess.Afternoon).all()
    Evening = session.query(Mess.Evening).all()
    Dinner = session.query(Mess.Dinner).all()
    Availability = session.query(Mess.Availability).all()
    Quality = session.query(Mess.Quality).all()
    Behaviour = session.query(Mess.Behaviour).all()
    return render_template('admin/mess.html', Morning = Morning,
                            Afternoon = Afternoon, Evening = Evening,
                            Dinner = Dinner, Availability = Availability,
                            Quality = Quality, Behaviour = Behaviour)

@app.route('/admin/staff')
def AdminStaff():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if 'type' in term and not term['type'] == "admin":
        return redirect(url_for('Login'))
    Caretaker = session.query(staff.Caretaker).all()
    Wardens = session.query(staff.Wardens).all()
    Principal = session.query(staff.Principal).all()
    Behaviour = session.query(staff.Behaviour).all()
    Problems = session.query(staff.Problems).all()
    Rating = session.query(staff.Rating).all()
    return render_template('admin/staff.html', Caretaker = Caretaker,
                            Wardens = Wardens, Principal = Principal,
                            Behaviour = Behaviour, Problems = Problems, Rating = Rating)

@app.route('/admin/others')
def AdminOthers():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if 'type' in term and not term['type'] == "admin":
        return redirect(url_for('Login'))
    Availability = session.query(OtherFeedback.Availability).all()
    Services = session.query(OtherFeedback.Services).all()
    return render_template('admin/other.html', Availability = Availability,
                            Services = Services)

@app.route('/admin/facilities')
def AdminFacilites():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if 'type' in term and not term['type'] == "admin":
        return redirect(url_for('Login'))
    Room = session.query(FacilitiesFeedback.Room).all()
    Corridors = session.query(FacilitiesFeedback.Corridors).all()
    Toilets = session.query(FacilitiesFeedback.Toilets).all()
    Croom = session.query(FacilitiesFeedback.Croom).all()
    Lawns = session.query(FacilitiesFeedback.Lawns).all()
    return render_template('admin/facilities.html', Room = Room, Corridors = Corridors,
                            Toilets = Toilets, Croom = Croom, Lawns = Lawns)

@app.route('/admin/water')
def AdminWater():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if 'type' in term and not term['type'] == "admin":
        return redirect(url_for('Login'))
    water = session.query(Water.Water).all()
    Quality = session.query(Water.Quality).all()
    Quantity = session.query(Water.Quantity).all()
    Variety = session.query(Water.Variety).all()
    Cost = session.query(Water.Cost).all()
    return render_template('admin/water.html', water = water, Quality = Quality,
                            Quantity = Quantity, Variety = Variety, Cost = Cost)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "helkjrofidjojoidjgoivjdfio"
    app.run(host = '0.0.0.0', port = 8000)
