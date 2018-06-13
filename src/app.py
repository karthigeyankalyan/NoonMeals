from src.common.database import Database
from src.models.employee import Employee
from flask import Flask, render_template, request, session, make_response

import json
from bson import json_util
from bson.objectid import ObjectId
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

@app.route('/raw_retirement_by_date/<string:date>')
def retiring_this_month(date):
    date_filter = date.replace("_", "/")
    projects = Database.find("employees", {"Date of Retirement": date_filter})
    json_projects = []
    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring

@app.route('/get_retirement', methods=['POST', 'GET'])
def retirement_by_date():
    if request.method == 'GET':
        return render_template('get_date.html')
    else:
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']

        date = day+"_"+month+"_"+year

        return render_template('retired_on_date.html', date=date)

@app.route('/raw_ttt/<string:month>/<string:year>')
def ttw_this_month(month, year):
    year10 = year - 10
    year20 = year - 20
    year30 = year - 30

    projects = Database.find("employees", {"$or": [
        {"$and": [{"Date of Joining": '/' + year10 + '$/'}, {"Date of Joining": '/^' + month + '/'}]},
        {"$and": [{"Date of Joining": '/' + year20 + '$/'}, {"Date of Joining": '/^' + month + '/'}]},
        {"$and": [{"Date of Joining": '/' + year30 + '$/'}, {"Date of Joining": '/^' + month + '/'}]},
        {"$and": [{"Date of Joining": '/' + month + '$/'}, {"Date of Joining": '/^' + year10 + '/'}]},
        {"$and": [{"Date of Joining": '/' + month + '$/'}, {"Date of Joining": '/^' + year20 + '/'}]},
        {"$and": [{"Date of Joining": '/' + month + '$/'}, {"Date of Joining": '/^' + year30 + '/'}]},
    ]})

    print(year10)
    print(year20)
    print(year30)
    print(year, month)

    json_projects = []
    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring

@app.route('/get_tentwentythirty', methods=['POST', 'GET'])
def ttw_by_date():
    if request.method == 'GET':
        return render_template('get_month_date.html')
    else:
        month = request.form['month']
        year = request.form['year']

        return render_template('ttt_on_date.html', month=month, year=year)

@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/table')
def render_employees():
        projects = Database.find("employees", {})
        json_projects = []
        for project in projects:
            json_projects.append(project)
        all_employees_state = json.dumps(json_projects, default=json_util.default)

        return all_employees_state

@app.route('/employee_table/<string:_id>')
def render_individual_employees(_id):
    single_employee_array = []
    single_employee_dict = Database.find("employees", {'_id': ObjectId(_id)})
    for Emp in single_employee_dict:
        single_employee_array.append(Emp)

    single_employee_block = json.dumps(single_employee_array, default=json_util.default)

    return single_employee_block

@app.route('/block_table/<string:Block>')
def render_block_employees(Block):
    block_employees_array = []
    block_employees_dict = Database.find("employees", {'Block': Block})
    for Emp in block_employees_dict:
        block_employees_array.append(Emp)

    all_employees_block = json.dumps(block_employees_array, default=json_util.default)

    return all_employees_block

@app.route('/district_table/<string:District>')
def render_district(District):
    district_employees_array = []
    district_employees_dict = Database.find("employees", {'District': District})
    for Emp in district_employees_dict:
        district_employees_array.append(Emp)

    all_employees_state = json.dumps(district_employees_array, default=json_util.default)

    return all_employees_state

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

@app.route('/district_beneficiaries/<string:District>')
def all_district_employees(District):
    email = session['email']
    if email is not None:
        return render_template('all_beneficiaries.html', district=District)
    else:
        return render_template('login_fail.html')

@app.route('/block_beneficiaries/<string:Block>')
@app.route('/block_beneficiaries')
def block_employees(Block):
    return render_template('block_beneficiaries.html', block=Block)

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

