from flask import Flask
from flask import render_template
from flask import request
import random
from flask import abort
from flask import jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Table, String
from sqlalchemy import create_engine, MetaData
import logging

app = Flask(__name__)
app.secret_key = "Secret Key"

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levelname)s-%(message)s")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://narasimharaomeda:Mnrjr$14@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('mysql://narasimharaomeda:Mnrjr$14@localhost/test')
metadata = MetaData()

def db_table():
    table = Table('employees', metadata, autoload=True, autoload_with=engine)
    if 'employees' not in str(table):
        logging.info('Creating table employee')
        employees = Table('employees', metadata, 
                            Column('emp_id',String(20), primary_key=True),
                            Column('emp_name',String(30)),
                            Column('emp_age',Integer),
                            Column('emp_position',String(30)),
                            Column('emp_place', String(30)),
                            Column('employer', String(30)),
                            Column('emp_salary', Integer), extend_existing=True)
        metadata.create_all(engine)
        logging.info('created employee table')
    else:
        logging.info('Table exists skipping the creating table')

db = SQLAlchemy(app)

class employees(db.Model):
    emp_id = db.Column(db.String, primary_key=True)
    emp_name = db.Column(db.String)
    emp_age = db.Column(db.Integer)
    emp_position = db.Column(db.String)
    emp_place = db.Column(db.String)
    employer = db.Column(db.String)
    emp_salary = db.Column(db.Integer)

    def __init__(self, emp_id, emp_name, emp_age, emp_position, emp_place, employer, emp_salary):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.emp_age = emp_age
        self.emp_position = emp_position
        self.emp_place = emp_place
        self.employer = employer
        self.emp_salary = emp_salary
    
    def data(self):
        employee = {}
        employee['id'] = self.emp_id
        employee['name'] = self.emp_name
        employee['age'] = self.emp_age
        employee['place'] = self.emp_place
        employee['position'] = self.emp_position
        employee['employer'] = self.employer
        employee['salary'] = self.emp_salary
        return employee


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/postdata')
def postdata():
    return render_template('postdata.html')

@app.route('/getdata')
def getdata():
    return render_template('getdata.html')

@app.route('/saved', methods=['POST','GET'])
def saved():
    if request.method == 'POST':    
        id_ = request.form['id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        place = request.form['place']
        salary = request.form['salary']
        employer = request.form['employer']

        logging.info('Request made to add the employees data in the database')
        #logging.info(f'[ID {id_}, Name:{name}, Age:{age}, Position:{position}, Place:{place}, Salary: {salary}, Employer:{employer}]')

        data = employees(id_, name, age, position, place, employer, salary)
        db.session.add(data)
        db.session.commit() 


        return render_template('saved.html',id_=id_)
    else:
        return abort(400)

@app.route('/data', methods=['POST','GET'])
def data():
    
    if request.method == 'GET':
        id_ = request.args.get('userid')
        user_data = employees.query.get(id_)
        employee = user_data.data()
        return jsonify(json.dumps(employee))
    else:
        return abort(400)



def main():
    if __name__ == '__main__':
        db_table()
        app.run(debug=True)

main()


