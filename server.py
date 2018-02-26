from flask import Flask, render_template, url_for, request
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, OtherFeedback, FacilitiesFeedback, Water, Mess, staff

engine = create_engine('sqlite:///feedback.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/feedback')
def Feedback():
    return render_template('feedback.html')

@app.route('/feedback/staff', methods = ['GET', 'POST'])
def StaffFeedback():
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
    app.run(host = '0.0.0.0', port = 8000)
