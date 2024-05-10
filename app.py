from flask import Flask , render_template,url_for,request ,jsonify,redirect,session
from math import sin,cos,tan,sqrt,pow
import bcrypt  # Secure hashing library
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = '123'



club_members = db.Table('club_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True)
)
# User model (replace with your model definition if using a database)
class User(db.Model):
  __tablename__ = 'user'  # Explicit table name definition
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(80), unique=True, nullable=False)
  username = db.Column(db.String(40), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  account_type = db.Column(db.String(20), nullable=False)
  clubs = db.relationship('Club', secondary=club_members, backref=db.backref('participants', lazy='dynamic'))

    # Add methods for password hashing and verification here

  def __init__(self, email, username, password, account_type):
    self.email = email
    self.username = username
    self.password_hash = self.hash_password(password)
    self.account_type = account_type

  def hash_password(self, password):
    # Use bcrypt to hash password securely
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  def verify_password(self, password):
    # Verify password using bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
  

class Club(db.Model):
    __tablename__ = 'club'  # Explicit table name definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    head = db.Column(db.Integer, db.ForeignKey('user.id'))  # Ensure this matches the User table name

    club_head = db.relationship('User', backref='headed_clubs')
    members = db.relationship('User', secondary=club_members, backref=db.backref('joined_clubs', lazy='dynamic'))


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

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    club = db.relationship('Club', backref=db.backref('announcements', lazy=True))

# Assuming the head of the club is the same as the user who created the event/announcement
# You can add a new event or announcement by a club head like this:












# Create database tables (assuming models are defined)
with app.app_context():
    db.create_all()  # Create tables for the default database
 # Create tables for the 'clubs' bind

def create_tables():
    with app.app_context():
        db.create_all()

####################################################################################
####################################################################################
####################################################################################








##creating roots=links=URL
#main route

@app.route('/')
def main():
    print("Current session username:", session.get('username', 'Guest'))  # Debug print
    return render_template("app.html", user=session.get('username', 'Guest'))


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")







@app.route('/get_club_requests', methods=['GET'])
def get_club_requests():
    # Fetch all club requests from the database
    requests = ClubRequest.query.all()

    # Serialize the requests to JSON format
    serialized_requests = [{
        'id': request.id,
        'user_id': request.user_id,
        'club_name': request.club_name,
        'club_description': request.club_description,
        'club_image_url': request.club_image_url,
        'status': request.status
    } for request in requests]

    return jsonify(serialized_requests)


#########################
##########################
##########################
@app.route("/addnewclub", methods=['GET', 'POST'])

def addnewclub():
 if request.method == 'GET':
        return render_template('addnewclub.html')  # Render signup form template
 elif request.method == 'POST':
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

        # Check if a request for the same club already exists
        existing_request = ClubRequest.query.filter_by(user_id=user.id, club_name=club_name).first()
        if existing_request:
            return jsonify({'success': False, 'message': 'Club request already exists'}), 409

        try:
            # Create a new club request
            new_request = ClubRequest(
                user_id=user.id,
                club_name=club_name,
                club_description=club_description,
                club_image_url=club_image_url
            )
            db.session.add(new_request)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Club request submitted successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
     else:
        return jsonify({'success': False, 'message': 'Request must be JSON'}), 400
#########################
##########################
##########################
@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/About")
def About():
    return render_template("About.html")


@app.route("/olduser")
def olduser():
    if 'user_id' in session:  # Check if user is logged in
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            clubs = Club.query.filter_by(head=user_id).all()  # Fetch clubs where the user is the head
            print(user.username)
            return render_template("olduser.html", user=user, clubs=clubs)
    return redirect('/')

@app.route("/newclub/<int:club_id>")
def newclub(club_id):
    club = Club.query.get(club_id)
    

    # Check if the club exists
    if club:
        # Access the head of the club
        head_user = club.club_head

        # Check if the head user exists
        if head_user:
            # Extract the email of the head
            head_email = head_user.email
        else:
            # Handle case where head user does not exist
            head_email = "No head assigned"

        # Check if the user has joined the club
        user_joined_club = False
        is_club_head = False  # New condition for checking if the user is the head of the club
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user:
                # Check if the user is the head of the club
                if club.head == user_id:
                    is_club_head = True
                # Check if the user has joined the club
                if club in user.joined_clubs:
                    user_joined_club = True

        return render_template('newclub.html', club=club, head_email=head_email, user_joined_club=user_joined_club, is_club_head=is_club_head)
    else:
        # Handle case where club does not exist
        return render_template('newclub.html', club=None, head_email="Club not found", user_joined_club=False, is_club_head=False)

@app.route("/student")
def student():
    if 'user_id' in session:  # Check if user is logged in
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            clubs = Club.query.filter_by(head=user_id).all()  # Fetch clubs where the user is the head
            print(user.username)
            return render_template("student.html", user=user, clubs=clubs)

@app.route("/clubmanager")
def clubmanager():
    if 'user_id' in session:  # Check if user is logged in
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            clubs = Club.query.filter_by(head=user_id).all()  # Fetch clubs where the user is the head
            print(user.username)
            return render_template("clubmanager.html", user=user, clubs=clubs)

@app.route("/Clubs")
def Clubs():
    return render_template("Clubs.html")

@app.route("/soc")
def soc():
    return render_template("soc.html")



@app.route("/Events", methods=['POST'])
def add_event():
    data = request.get_json()
    club_id = data.get('club_id')
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')

    # Check if the club exists and the logged-in user is the head of the club
    user_id = session.get('user_id')
    club = Club.query.filter_by(id=club_id, head=user_id).first()

    if not club:
        return jsonify({'success': False, 'message': 'Club not found or user is not the head of the club'}), 404

    # Create and add the event to the club
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
##Samas code:
############################
############################
############################
############################
############################
############################
@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('Signup.html')  # Render signup form template
    elif request.method == 'POST':
        # In your signup function
        data = request.get_json()  # Assuming data is sent as JSON
        email = data.get('email')  # Access email from JSON object
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        account_type = data.get('account_type')

        # Basic validation
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

        # Check for existing user (assuming User model)
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            errors.append("Username or email already exists.")

        if errors:  # If there are errors, return them to the client
            return jsonify({'success': False, 'errors': errors}), 400

        # Create new user if no errors
        new_user = User(email=email, username=username, password=password, account_type=account_type)
        db.session.add(new_user)
        db.session.commit()

        # Respond success
        return jsonify({'success': True, 'message': 'User created successfully'}), 201

    return 'Something went wrong.', 500  # Handle unexpected cases




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Display the login form
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Please fill in all fields.'}), 400

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            session['user_id'] = user.id  # Set user ID in session
            session['username'] = user.username 
            print("Login successful, session username:", session['username'])
            return jsonify({'success': True, 'message': 'Login successful', 'account_type': user.account_type})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

############################    
############################
############################
############################
############################
############################


if __name__ == "__main__":
    with app.app_context():
      create_tables()
      app.run(debug=True)