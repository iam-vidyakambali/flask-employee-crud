from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        new_emp = Employee(name=name, department=department, email=email)
        db.session.add(new_emp)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    emp = Employee.query.get_or_404(id)
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.department = request.form['department']
        emp.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', emp=emp)

@app.route('/delete/<int:id>')
def delete(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
