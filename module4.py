from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercise_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Exercise model
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now)
    exercise_key = db.Column(db.String(50), nullable=False)  # Changed from common_key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Health Measurement model
class HealthMeasurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    bmi = db.Column(db.Float)
    upper_arms = db.Column(db.Float)
    forearms = db.Column(db.Float)
    shoulders = db.Column(db.Float)
    chest = db.Column(db.Float)
    stomach = db.Column(db.Float)
    thighs = db.Column(db.Float)
    calves = db.Column(db.Float)
    date_time = db.Column(db.DateTime, default=datetime.now)
    health_measurement_key = db.Column(db.String(50), nullable=False)  # Changed from common_key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes

# Home route, requires user authentication
@app.route('/')
@login_required
def index():
    # Get start and end dates for the time range
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Default to the last 10 entries if no date range is specified
    default_start_date = datetime.now() - timedelta(days=30)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else default_start_date
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else datetime.now()

    # Query exercises within the specified date range
    exercises = Exercise.query.filter(
        Exercise.user_id == current_user.id,
        Exercise.exercise_key.between(start_date, end_date)
    ).order_by(Exercise.exercise_key.desc()).limit(10).all()

    # Query health measurements within the specified date range
    health_measurements = HealthMeasurement.query.filter(
        HealthMeasurement.user_id == current_user.id,
        HealthMeasurement.health_measurement_key.between(start_date, end_date)
    ).order_by(HealthMeasurement.health_measurement_key.desc()).limit(10).all()

    # Render the template with the retrieved data
    return render_template('index.html', exercises=exercises, health_measurements=health_measurements)

# Route for adding a new exercise
@app.route('/add_exercise', methods=['POST'])
@login_required
def add_exercise():
    # Retrieve form data
    name = request.form['name']
    reps = int(request.form['reps'])
    sets = int(request.form['sets'])
    weight = float(request.form['weight'])

    # Validate form inputs
    if not name or reps <= 0 or sets <= 0 or weight <= 0:
        flash('Invalid input. Please fill out all fields with valid values.', 'error')
        return redirect(url_for('index'))

    # Generate a unique exercise key using the current date and time
    exercise_key = datetime.now()

    # Create a new Exercise object and add it to the database
    new_exercise = Exercise(name=name, reps=reps, sets=sets, weight=weight, user_id=current_user.id, exercise_key=exercise_key)
    db.session.add(new_exercise)
    db.session.commit()

    # Flash a success message and redirect to the home page
    flash('Exercise added successfully!', 'success')
    return redirect(url_for('index'))

# Route for adding a new health measurement
@app.route('/add_health_measurement', methods=['POST'])
@login_required
def add_health_measurement():
    # Retrieve form data
    weight = float(request.form['weight'])
    bmi = float(request.form['bmi'])
    upper_arms = float(request.form['upper_arms'])
    forearms = float(request.form['forearms'])
    shoulders = float(request.form['shoulders'])
    chest = float(request.form['chest'])
    stomach = float(request.form['stomach'])
    thighs = float(request.form['thighs'])
    calves = float(request.form['calves'])

    # Validate form inputs
    if weight <= 0 or bmi <= 0 or upper_arms <= 0 or forearms <= 0 or shoulders <= 0 or \
            chest <= 0 or stomach <= 0 or thighs <= 0 or calves <= 0:
        flash('Invalid input. Please fill out all fields with valid values.', 'error')
        return redirect(url_for('index'))

    # Generate a unique health measurement key using the current date and time
    health_measurement_key = datetime.now()

    # Create a new HealthMeasurement object and add it to the database
    new_health_measurement = HealthMeasurement(
        weight=weight,
        bmi=bmi,
        upper_arms=upper_arms,
        forearms=forearms,
        shoulders=shoulders,
        chest=chest,
        stomach=stomach,
        thighs=thighs,
        calves=calves,
        user_id=current_user.id,
        health_measurement_key=health_measurement_key
    )

    db.session.add(new_health_measurement)
    db.session.commit()

    # Flash a success message and redirect to the home page
    flash('Health measurement added successfully!', 'success')
    return redirect(url_for('index'))

# New route for exercise and health summary
@app.route('/exercise_health_summary')
@login_required
def exercise_health_summary():
    # Perform a join operation between Exercise and HealthMeasurement tables
    joined_data = db.session.query(
        Exercise.name,
        Exercise.reps,
        Exercise.sets,
        Exercise.weight,
        HealthMeasurement.weight.label('health_weight'),
        HealthMeasurement.bmi
    ).join(
        HealthMeasurement,
        Exercise.exercise_key == HealthMeasurement.health_measurement_key
    ).filter(
        Exercise.user_id == current_user.id,
        HealthMeasurement.user_id == current_user.id
    ).all()

    # Use aggregate functions to summarize numerical data
    total_reps = func.sum(Exercise.reps).label('total_reps')
    average_weight = func.avg(Exercise.weight).label('average_weight')
    max_bmi = func.max(HealthMeasurement.bmi).label('max_bmi')

    # Query aggregated summary data
    summary_data = db.session.query(
        total_reps,
        average_weight,
        max_bmi
    ).filter(
        Exercise.user_id == current_user.id,
        HealthMeasurement.user_id == current_user.id
    ).first()

    # Render the template with the joined data and summary data
    return render_template('exercise_health_summary.html', joined_data=joined_data, summary_data=summary_data)

if __name__ == '__main__':
    # Create database tables if they don't exist and run the application in debug mode
    db.create_all()
    app.run(debug=True)
