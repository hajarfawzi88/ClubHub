from flask import Flask, render_template, request, redirect, url_for
import bcrypt  # Secure hashing library
from flask_sqlalchemy import SQLAlchemy
# Flask app setup
app = Flask(__name__)

# Configure database (replace with your connection details)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database (assuming a User model)
db = SQLAlchemy(app)

# User model (replace with your model definition if using a database)
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(80), unique=True, nullable=False)
  username = db.Column(db.String(40), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  account_type = db.Column(db.String(20), nullable=False)

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

# Create database tables (assuming models are defined)
with app.app_context():
    db.create_all()
# Signup form route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup/Signup.html')  # Render signup form template

  elif request.method == 'POST':
   # In your signup function
    data = request.get_json()  # Assuming data is sent as JSON
    email = data.get('email')  # Access email from JSON object
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    account_type = data.get('account_type')

    # Basic validation
    if not email or not username or not password or not confirm_password:
      return render_template('signup/Signup.html', error="Please fill out all fields.")
    if password != confirm_password:
      return render_template('signup/Signup.html', error="Passwords do not match.")

    # Check for existing user (assuming User model)
    existing_user = User.query.filter_by(username=username).filter_by(email=email).first()

    if existing_user:
      return render_template('signup/Signup.html', error="Username or email already exists.")

    # # Create new user object (assuming User model)
    new_user = User(email, username, password, account_type)

    # Add user to database and commit changes
    db.session.add(new_user)
    db.session.commit()

    # Handle successful registration (e.g., redirect to login page, send confirmation email)
    return 'success!!'  # Example redirect to login page (implement login route later)

  return 'Something went wrong.'  # Handle unexpected cases

# Run the Flask app (modify host and port if needed)
if __name__ == '__main__':
  app.run(debug=True, host='localhost', port=5000)
