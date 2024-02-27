from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_cars.db'
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f'<Booking {self.id}>'

@app.route('/', methods=['GET'])
def index():
    bookings = Booking.query.all()
    return render_template('index.html', bookings=bookings)

@app.route('/add', methods=['POST'])
def add_booking():
    employee_id = request.form['employee_id']
    purpose = request.form['purpose']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    new_booking = Booking(employee_id=employee_id, purpose=purpose, start_time=start_time, end_time=end_time)
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.employee_id = request.form['employee_id']
    booking.purpose = request.form['purpose']
    booking.start_time = request.form['start_time']
    booking.end_time = request.form['end_time']

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('index'))
update_booking(1)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)
