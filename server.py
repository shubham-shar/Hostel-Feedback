from flask import Flask, render_template, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/feedback')
def hello():
    return render_template('feedback.html')

@app.route('/feedback/staff')
def StaffFeedback():
    return render_template('staff.html')

@app.route('/feedback/room')
def WaterFeedback():
    return render_template('water.html')

@app.route('/feedback/mess')
def MessFeedback():
    return render_template('mess.html')

@app.route('/feedback/facilities')
def Facilities():
    return render_template('facilities.html')

@app.route('/feedback/others')
def Others():
    return render_template('others.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
