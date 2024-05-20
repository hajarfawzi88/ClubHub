from flask import Flask, render_template, url_for, request, jsonify, redirect, session, flash
from math import sin, cos, tan, sqrt, pow
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask app using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

# Association table for many-to-many relationship between User and Club
club_members = db.Table('club_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    
    # Relationships
    headed_clubs = db.relationship('Club', backref='head')
    memberships = db.relationship('Membership', back_populates='user', overlaps="clubs")
    clubs = db.relationship('Club', secondary=club_members, back_populates='members', overlaps="memberships")

    def __init__(self, email, username, password, account_type):
        self.email = email
        self.username = username
        self.password_hash = self.hash_password(password)
        self.account_type = account_type

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024))
    image_url = db.Column(db.String(255))
    head_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    members = db.relationship('User', secondary=club_members, back_populates='clubs', overlaps="memberships")
    memberships = db.relationship('Membership', back_populates='club', overlaps="members, clubs")

class Membership(db.Model):
    __tablename__ = 'membership'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), primary_key=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='memberships', overlaps="clubs")
    club = db.relationship('Club', back_populates='memberships', overlaps="members,clubs")

class ClubRequest(db.Model):
    __tablename__ = 'club_request'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('requests', lazy=True))
    club_name = db.Column(db.String(100), nullable=False)
    club_description = db.Column(db.String(300), nullable=False)
    club_image_url = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # Status of the request (pending, approved, rejected)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', backref=db.backref('events', lazy=True))
    location = db.Column(db.String(100), nullable=False)
    expected_members = db.Column(db.Integer, nullable=False)

class EventRequest(db.Model):
    __tablename__ = 'event_request'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    expected_members = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', backref=db.backref('event_requests', lazy=True))

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', backref=db.backref('announcements', lazy=True))

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1024))
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

User.clubs = db.relationship('Club', secondary='membership', back_populates='members')

# Create database tables (assuming models are defined)
with app.app_context():
    db.create_all()  # Create tables for the default database

def create_tables():
    with app.app_context():
        db.create_all()

# Define routes and view functions
@app.route('/')
def main():
    print("Current session username:", session.get('username', 'Guest'))  # Debug print
    return render_template("app.html", user=session.get('username', 'Guest'))

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route('/Editprofile', methods=['POST', 'GET'])
def Editprofile():
    if request.method == 'GET':
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user:
                return render_template("Editprofile.html", user=user)
            else:
                return 'User not found', 404

    elif request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'success': False, 'errors': ['User not found']}), 404

            data = request.get_json()
            email = data.get('email')
            username = data.get('username')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_new_password = data.get('confirm_new_password')

            errors = []

            if email:
                if not isValidEmail(email):
                    errors.append("Please enter a valid email address.")
                elif User.query.filter(User.email == email, User.id != user_id).first():
                    errors.append("Email already exists.")
                else:
                    user.email = email

            if username:
                if len(username) < 6:
                    errors.append("Username must be at least 6 characters long.")
                elif User.query.filter(User.username == username, User.id != user_id).first():
                    errors.append("Username already exists.")
                else:
                    user.username = username

            if old_password and new_password and confirm_new_password:
                if not user.verify_password(old_password):
                    errors.append("Old password is incorrect.")
                elif new_password != confirm_new_password:
                    errors.append("New passwords do not match.")
                elif not isValidPassword(new_password):
                    errors.append("New password must be at least 8 characters long and include a mix of uppercase, lowercase letters, numbers, and symbols.")
                else:
                    user.password_hash = user.hash_password(new_password)

            if errors:
                return jsonify({'success': False, 'errors': errors}), 400

            db.session.commit()
            return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200

    return 'Something went wrong.', 500

def isValidEmail(email):
    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(email_regex, email) is not None

def isValidPassword(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None

@app.route('/Editclub/<int:club_id>', methods=['GET', 'POST'])
def Editclub(club_id):
    club = Club.query.get(club_id)
    if not club:
        return 'Club not found', 404

    if 'user_id' not in session or club.head_id != session['user_id']:
        return 'Unauthorized', 403

    if request.method == 'GET':
        return render_template("Editclub.html", club=club)

    elif request.method == 'POST':
        data = request.form  # Use form data instead of JSON
        club.name = data.get('name', club.name)
        club.description = data.get('description', club.description)
        club.image_url = data.get('image_url', club.image_url)
        
        db.session.commit()
        return redirect(url_for('newclub', club_id=club_id))

@app.route('/get_club_requests', methods=['GET'])
def get_club_requests():
    requests = ClubRequest.query.all()  # Fetch all requests (adjust according to your data model)
    serialized_requests = [{
        'id': req.id,
        'club_name': req.club_name,
        'club_description': req.club_description,
        'username': req.user.username,  # Assuming each request is associated with a user
        'status': req.status
    } for req in requests]
    return jsonify(serialized_requests)

@app.route("/addnewclub", methods=['GET', 'POST'])
def addnewclub():
    if request.method == 'GET':
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            users = User.query.all()
            clubs = Club.query.all()
            return render_template('addnewclub.html', user=user, users=users, clubs=clubs)
    elif request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if not user:
                return jsonify({'success': False, 'errors': ['User not found']}), 404
        if request.is_json:
            data = request.get_json()
            head_email = data.get('head_email')
            club_name = data.get('name')
            club_description = data.get('description')
            club_image_url = data.get('image_url')

            if not all([head_email, club_name, club_description, club_image_url]):
                return jsonify({'success': False, 'message': 'All fields are required'}), 400

            user = User.query.filter_by(email=head_email).first()
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404

            existing_request = ClubRequest.query.filter_by(club_name=club_name).first()
            existing_club = Club.query.filter_by(name=club_name).first()
            if existing_request or existing_club:
                return jsonify({'success': False, 'message': 'Club name already in use'}), 409

            try:
                new_request = ClubRequest(
                    user_id=user.id,
                    club_name=club_name,
                    club_description=club_description,
                    club_image_url=club_image_url,
                    status='pending'
                )
                db.session.add(new_request)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Club request submitted successfully'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': str(e)}), 500
        else:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

@app.route('/approve_request', methods=['POST'])
def approve_request():
    data = request.get_json()
    request_id = data.get('request_id')

    request_data = ClubRequest.query.get(request_id)
    if not request_data:
        return jsonify({'success': False, 'message': 'Club request not found'}), 404

    existing_club = Club.query.filter_by(name=request_data.club_name).first()
    if existing_club:
        db.session.delete(request_data)
        db.session.commit()
        return jsonify({'success': False, 'message': 'A club with this name already exists'}), 409

    try:
        head_user = User.query.get(request_data.user_id)
        if not head_user:
            db.session.delete(request_data)
            db.session.commit()
            return jsonify({'success': False, 'message': 'Head user not found'}), 404

        new_club = Club(
            name=request_data.club_name,
            description=request_data.club_description,
            image_url=request_data.club_image_url,
            head_id=head_user.id
        )
        db.session.add(new_club)
        db.session.delete(request_data)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Club request approved and club created successfully, head assigned'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/deny_request', methods=['POST'])
def deny_request():
    data = request.get_json()
    request_id = data.get('request_id')

    request_data = ClubRequest.query.get(request_id)

    if request_data:
        db.session.delete(request_data)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Club request denied and removed successfully'}), 200
    else:
        return jsonify({'success': False, 'message': 'Club request not found'}), 404

@app.route('/RequestEvents', methods=['GET', 'POST'])
def RequestEvents():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    if not user:
        return redirect('/login')

    if request.method == 'POST':
        eventName = request.form.get('eventName')
        location = request.form.get('location')
        expectedMembers = request.form.get('expectedMembers')
        date = request.form.get('date')

        if not all([eventName, location, expectedMembers, date]):
            flash('All fields are required.', 'error')
            return redirect(url_for('RequestEvents'))

        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('RequestEvents'))

        new_event = Event(name=eventName, location=location, date=date, expected_members=expectedMembers)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')

    clubs_info = []
    member_clubs = user.clubs
    headed_clubs = Club.query.filter_by(head_id=user_id).all()
    all_clubs = set(member_clubs + headed_clubs)

    for club in all_clubs:
        role = "Head" if club in headed_clubs else "Member"
        events = [event for event in club.events]
        club_details = {
            'club': club,
            'role': role,
            'events': events
        }
        clubs_info.append(club_details)

    return render_template("RequestEvents.html", user=user, clubs_info=clubs_info, events=events)

@app.route('/get_event_requests', methods=['GET'])
def get_event_requests():
    event_requests = EventRequest.query.all()
    serialized_requests = [{
        'id': request.id,
        'name': request.event_name,
        'description': request.location,
        'date': request.date.strftime("%Y-%m-%d"),
        'expected_members': request.expected_members,
        'status': request.status,
        'club_name': request.club.name
    } for request in event_requests]
    return jsonify(serialized_requests)

@app.route('/submit_event_request', methods=['POST'])
def submit_event_request():
    data = request.get_json()
    eventName = data.get('eventName')
    location = data.get('location')
    expectedMembers = data.get('expectedMembers')
    description = data.get('description')
    eventDate = data.get('date')

    try:
        date = datetime.strptime(eventDate, '%m/%d/%Y')
    except ValueError as e:
        return jsonify({'message': 'Invalid date format', 'error': str(e)}), 400

    new_event = Event(name=eventName, location=location, date=date, expected_members=expectedMembers, description=description)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Your event request has been received and is pending approval.'})

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/About")
def About():
    return render_template("About.html")

@app.route("/olduser")
def olduser():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            clubs = []
            member_clubs = user.clubs
            headed_clubs = Club.query.filter_by(head_id=user_id).all()
            for club in set(member_clubs + headed_clubs):
                role = "Head" if club in headed_clubs else "Member"
                clubs.append({'club': club, 'role': role})

            return render_template("olduser.html", user=user, clubs=clubs)
    return redirect('/')

@app.route("/newclub/<int:club_id>", methods=['GET', 'POST'])
def newclub(club_id):
    if request.method == 'GET':
        club = Club.query.get(club_id)
        if not club:
            return render_template('newclub.html', club=None, message="Club not found")

        head_email = club.head.email if club.head else "No head assigned"
        user_joined_club = False
        is_club_head = False

        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user:
                is_club_head = (club.head_id == user_id)
                user_joined_club = user in club.members

        can_view_details = is_club_head or user_joined_club

        return render_template('newclub.html', club=club, head_email=head_email, can_view_details=can_view_details, is_club_head=is_club_head)
    elif request.method == 'Post':
        data = request.get_json()
        request_id = data.get('request_id')

        request_data = ClubRequest.query.get(request_id)
        if not request_data:
            return jsonify({'success': False, 'message': 'Club request not found'}), 404

        existing_club = Club.query.filter_by(name=request_data.club_name).first()
        if existing_club:
            db.session.delete(request_data)
            db.session.commit()
            return jsonify({'success': False, 'message': 'A club with this name already exists'}), 409

        try:
            head_user = User.query.get(request_data.user_id)
            if not head_user:
                db.session.delete(request_data)
                db.session.commit()
                return jsonify({'success': False, 'message': 'Head user not found'}), 404

            new_club = Club(
                name=request_data.club_name,
                description=request_data.club_description,
                image_url=request_data.club_image_url,
                head_id=head_user.id
            )
            db.session.add(new_club)
            db.session.delete(request_data)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Added successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/student")
def student():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            member_clubs = user.clubs
            headed_clubs = Club.query.filter_by(head_id=user_id).all()
            clubs = list(set(member_clubs + headed_clubs))
            all_clubs = Club.query.all()

            return render_template("student.html", user=user, all_clubs=all_clubs, clubs=clubs)
    return redirect('/')

@app.route("/clubmanager")
def clubmanager():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            clubs = Club.query.filter(Club.head_id == user_id).all()
            return render_template("clubmanager.html", user=user, clubs=clubs)
    return redirect('/')

@app.route("/Clubs")
def Clubs():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            member_clubs = user.clubs
            headed_clubs = Club.query.filter_by(head_id=user_id).all()
            clubs = list(set(member_clubs + headed_clubs))
            return render_template("Clubs.html", user=user, clubs=clubs)
    return redirect('/')

@app.route("/soc")
def soc():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            clubs = Club.query.filter(Club.head_id == user_id).all()
            return render_template("soc.html", user=user, clubs=clubs)
    return redirect('/')

@app.route("/Events", methods=['POST'])
def add_event():
    data = request.get_json()
    club_id = data.get('club_id')
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')

    user_id = session.get('user_id')
    club = Club.query.filter_by(id=club_id, head=user_id).first()

    if not club:
        return jsonify({'success': False, 'message': 'Club not found or user is not the head of the club'}), 404

    event = Event(name=name, description=description, date=date, club_id=club_id)
    db.session.add(event)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Event added successfully'}), 201

@app.route("/Announcements")
def Announcements():
    return render_template("Announcements.html")

@app.route("/userprofile")
def userprofile():
    return render_template("userprofile.html")

@app.route("/joinnewclub")
def joinnewclub():
    return render_template("joinnewclub.html")

@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('Signup.html')
    elif request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        account_type = data.get('account_type')

        errors = []
        if not email:
            errors.append("Email is required.")
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if not confirm_password:
            errors.append("Confirm password is required.")
        if password != confirm_password:
            errors.append("Passwords do not match.")

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            errors.append("Username or email already exists.")

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        new_user = User(email=email, username=username, password=password, account_type=account_type)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User created successfully'}), 201

    return 'Something went wrong.', 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            return jsonify({'success': True, 'message': 'Login successful', 'account_type': user.account_type}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

    
if __name__ == "__main__":
    with app.app_context():
        port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT not set
        app.run(host='0.0.0.0', port=port)
