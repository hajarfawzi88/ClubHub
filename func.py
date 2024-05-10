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



@app.route('/x', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('x.html')  # Display the login form
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