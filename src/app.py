from src.common.database import Database
from src.models.employee import Employee
from flask import Flask, render_template, request, session, make_response

import json
from bson import json_util
from bson.json_util import dumps

from src.models.user import User

app = Flask(__name__)  #main
app.secret_key = "commercial"

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/beneficiary_plots')
def beneficiary_plots():
    return render_template('circle1.html')

@app.route('/district_plots/sanctioned')
def district_pension():
    return render_template('district_plots.html')

@app.route('/district_plots/eligible')
def district_pension_eligible():
    return render_template('district_plots_eligible.html')

@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/table')
def render_employees():
        projects = Database.find("employees", {})
        json_projects = []
        for project in projects:
            json_projects.append(project)
        json_projects = json.dumps(json_projects, default=json_util.default)

        return json_projects

@app.route('/district_table')
def render_district():
        projects = Database.find("district_nmp", {})
        district = []
        for project in projects:
            district.append(project)
        district = json.dumps(district, default=json_util.default)

        return district

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/authorize/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    valid = User.valid_login(email, password)
    User.login(email)
    user = User.get_by_email(email)

    if valid:
        return render_template('profile.html', user=user)

    else:
        return render_template('login_fail.html')

@app.route('/authorize/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    User.register(email, password, username)

    user = User.get_by_email(email)

    return render_template('profile.html', user=user)

@app.route('/profile_landing')
def profileLanding():
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        return render_template('profile.html', user=user)

@app.route('/all_beneficiaries')
def all_employees():
    email = session['email']
    if email is not None:
        employee = Employee.from_mongo_blog()
        return render_template('all_beneficiaries.html', employee=employee)

@app.route('/block_beneficiaries/<string:Block>')
@app.route('/block_beneficiaries')
def block_employees(Block):
    block_employees_array = []
    block_employees_dict = Database.find("employees", {'Block': Block})
    for Emp in block_employees_dict:
        block_employees_array.append(Emp)
    json_projects = json.dumps(block_employees_array, default=json_util.default)
    return render_template('abc.html', block=Block, emp=block_employees_array)

@app.route('/retirement_employees')
def retired_employees():
    return render_template('retirement_employees.html')

@app.route('/retired/block_employees/<string:Block>')
def retired_block_employees(Block):
    return render_template('retired_block_employees.html', block=Block)

@app.route('/new_employee/<string:_id>', methods=['POST', 'GET'])
def my_entries(_id):
    if request.method == 'GET':
        return render_template('form.html', _id=_id)
    else:
        district = request.form['district']
        name = request.form['name']
        block = request.form['block']
        panchayat = request.form['panchayat']
        center = request.form['center']
        DOB = request.form['DOB']
        qualification = request.form['qualification']
        joiningDate = request.form['joiningDate']
        designation = request.form['designation']
        retirementDate = request.form['retirementDate']

        employee = Employee(district=district, name=name, block=block, panchayat=panchayat, center_name=center,
                            DOB=DOB, qualification=qualification, joining_date=joiningDate, designation=designation,
                            retirement_date=retirementDate)

        employee.save_to_mongo()

        return render_template('beneficiary_added.html', employee=employee)

@app.route('/update_employee/<string:_id>', methods=['POST', 'GET'])
def update_entries(_id):
    if request.method == 'GET':
        return render_template('edit_employee_form.html', emp_id=_id)
    else:
        district = request.form['district']
        name = request.form['name']
        block = request.form['block']
        panchayat = request.form['panchayat']
        center = request.form['center']
        DOB = request.form['DOB']
        qualification = request.form['qualification']
        joiningDate = request.form['joiningDate']
        designation = request.form['designation']
        retirementDate = request.form['retirementDate']

        employee = Employee(district=district, name=name, block=block, panchayat=panchayat, center_name=center,
                            DOB=DOB, qualification=qualification, joining_date=joiningDate, designation=designation,
                            retirement_date=retirementDate)

        employee.update_employee(name=name, district=district, block=block, panchayat=panchayat,
                                 designation=designation, center_name=center, dob=DOB, doj=joiningDate,
                                 dor=retirementDate, emp_id=_id)

        return render_template('beneficiary_added.html', employee=employee)


if __name__=='__main__':
    app.run(port=4055, debug=True)

