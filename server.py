from flask import Flask, render_template, url_for, request, redirect
from flask import session as term
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, OtherFeedback, FacilitiesFeedback, Water, Mess, staff, Students

engine = create_engine('sqlite:///feedback.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/feedback')
def Feedback():
    return render_template('feedback.html')

@app.route('/signup', methods = ['GET', 'POST'])
def Signup():
    if 'logged_in' in term:
        return redirect(url_for('Feedback'))
    error = None
    if request.method == 'POST':
        password = request.form['Password']
        repass = request.form['Repass']
        email = request.form['Email']
        student = session.query(Students).filter_by(email = email).first()
        if student:
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
        student = session.query(Students).filter_by(email = request.form['Email']).first()
        if not student:
            error = "Signup First or check your email again"
            return render_template('login.html', error=error)
        elif not student.verify_password(request.form['Password']):
            error = "Wrong Password"
            return render_template('login.html', error=error)
        else:
            term['logged_in'] = True
            term['user_id'] = student.id
            term['email'] = student.email
            return redirect(url_for('Feedback'))
    else:
        return render_template('login.html', error=error)

@app.route('/logout')
def Logout():
    del term['logged_in']
    del term['user_id']
    del term['email']
    return redirect(url_for('Feedback'))

@app.route('/feedback/staff', methods = ['GET', 'POST'])
def StaffFeedback():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if request.method == 'POST':
        newFeedback = staff(Caretaker = request.form['Caretaker'],
                            Wardens = request.form['Wardens'],
                            Principal = request.form['Principal'],
                            Behaviour = request.form['Behaviour'],
                            Problems = request.form['Problems'],
                            Rating = request.form['Rating'])
        session.add(newFeedback)
        session.commit()
        return render_template('staff.html')
    else:
        return render_template('staff.html')

@app.route('/feedback/water', methods=['GET', 'POST'])
def WaterFeedback():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if request.method == 'POST':
        newFeedback = Water(Water = request.form['Water'],
                            Quality = request.form['Quality'],
                            Quantity = request.form['Quantity'],
                            Variety = request.form['Variety'],
                            Cost = request.form['Cost'])
        session.add(newFeedback)
        session.commit()
        return render_template('water.html')
    else:
        return render_template('water.html')

@app.route('/feedback/mess', methods=['GET', 'POST'])
def MessFeedback():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if request.method == 'POST':
        newFeedback = Mess(Morning = request.form['Morning'],
                           Afternoon = request.form['Afternoon'],
                           Evening = request.form['Evening'],
                           Dinner = request.form['Dinner'],
                           Availablity = request.form['Availability'],
                           Quality = request.form['Quality'],
                           Behaviour = request.form['Behaviour'])
        session.add(newFeedback)
        session.commit()
        return render_template('mess.html')
    else:
        return render_template('mess.html')

@app.route('/feedback/facilities', methods = ['GET','POST'])
def Facilities():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if request.method == 'POST':
        newFeedback = FacilitiesFeedback(Room = request.form['Room'],
                                        Corridors = request.form['Corridors'],
                                        Toilets = request.form['Toilets'],
                                        Croom = request.form['Croom'],
                                        Lawns = request.form['Lawns'])
        session.add(newFeedback)
        session.commit()
        return render_template('facilities.html')
    else:
        return render_template('facilities.html')

@app.route('/feedback/others', methods = ['GET', 'POST'])
def Others():
    if 'logged_in' not in term:
        return redirect(url_for('Login'))
    if request.method == 'POST':
        newFeedback = OtherFeedback(Availability = request.form['Availability'],
                                    Services = request.form['Services'])
        session.add(newFeedback)
        session.commit()
        return render_template('others.html')
    else:
        return render_template('others.html')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "helkjrofidjojoidjgoivjdfio"
    app.run(host = '0.0.0.0', port = 8000)
