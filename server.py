from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, OtherFeedback, FacilitiesFeedback, Water, Mess, staff, Students

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

engine = create_engine('sqlite:///feedback.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

CLIENT_ID = json.loads(
            open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hostel Feedback"

def createUser(login_session):
    newStudents = Students(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newStudents)
    session.commit()
    user = session.query(Students).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Students).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(Students).filter_by(email=email).one()
        return user.id
    except:
        return None

@app.route('/')
@app.route('/feedback')
def Feedback():
    return render_template('feedback.html')

@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gsignin', methods=['POST'])
def gsignin():
    if request.args.get('state') != login_session['state']:
        print 'invalid state parameter'
        return redirect(url_for('login'))
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        print 'failed to upgrade'
        return redirect(url_for('login'))

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        print 'error = ',result.get('error')
        return redirect(url_for('login'))

    g_id = credentials.id_token['sub']
    if result['user_id'] != g_id:
        print 'token user id doesnt match given user id'
        return redirect(url_for('login'))

    if result['issued_to'] != CLIENT_ID:
        print "Token's client ID does not match app's."
        return redirect(url_for('login'))

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        print 'user already connected'
        return redirect(url_for('/feedback'))

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = g_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'Google'

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += login_session['username']
    print "done!"
    return output

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
    app.secret_key = "alkjdfoiejgvkfjoj"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
