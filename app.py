from flask import Flask , render_template,url_for,request ,jsonify
from math import sin,cos,tan,sqrt,pow
import bcrypt  # Secure hashing library
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#creating sama's database:
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


####################################################################################
####################################################################################
####################################################################################








##creating roots=links=URL
#main route
@app.route("/")

def main():
    return render_template("app.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")



@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/About")
def About():
    return render_template("About.html")



@app.route("/cart")
def cart():
    return render_template("cart.html") 




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
    return render_template('login.html')  # Render signup form template
  elif request.method == 'POST':
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields.'}), 400  # Bad request

    # Query user by username
    with app.app_context():  # Ensure database session within request context
        user = db.session.query(User).filter_by(username=username).first()

    if not user:
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401  # Unauthorized

    # Validate password
    if not user.verify_password(password):
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401  # Unauthorized

    # Login successful (replace with actual session management or token generation)
    return jsonify({'success': True, 'message': 'Login successful!'}), 200  # OK

############################
############################
############################
############################
############################
############################


if __name__=="__main__":
    app.run(debug=True)
