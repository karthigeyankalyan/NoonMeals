import pandas as pd

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


@app.route('/employment_charts')
def beneficiary_plots():
    email = session['email']
    user = User.get_by_email(email)
    return render_template('district_plots.html', block=user.block, district=user.district)


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


@app.route('/raw_retirement_by_date_panmp/<string:date>/<string:District>')
def retiring_this_month_panmp(date, District):
    date_filter = date.replace("_", "/")
    projects = Database.find("employees", {"$and": [{"Date of Retirement": date_filter},
                                                    {"District": District}]})
    json_projects = []
    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/raw_retirement_by_date_block/<string:date>/<string:District>/<string:Block>')
def retiring_this_month_block(date, District, Block):
    date_filter = date.replace("_", "/")
    projects = Database.find("employees", {"$and": [{"Date of Retirement": date_filter},
                                                    {"District": District},
                                                    {"Block": Block}]})
    json_projects = []
    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/get_retirement_panmp/<string:District>', methods=['POST', 'GET'])
def retirement_by_date_panmp(District):
    if request.method == 'GET':
        return render_template('get_date_panmp.html', district=District)
    else:
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']

        date = day+"_"+month+"_"+year

        return render_template('retired_on_date_panmp.html', date=date, district=District)


@app.route('/change_password/<string:_id>', methods=['POST', 'GET'])
def change_password(_id):
    user = User.get_by_id(_id)
    if request.method == 'GET':
        return render_template('update_password.html', user=user)
    else:
        old_password = request.form['oldPassword']
        newPassword = request.form['newPassword']
        newPasswordAgain = request.form['newPasswordAgain']

    if user.password == old_password:
        if newPassword == newPasswordAgain:
            User.change_password(user._id, new_password=newPassword)
            return render_template('passwords_changed.html', user=user)
        else:
            return render_template('passwords_dont_match.html', user=user)
    else:
        return render_template('passwords_dont_match.html', user=user)


@app.route('/get_retirement_block/<string:District>/<string:Block>', methods=['POST', 'GET'])
def retirement_by_date_block(District, Block):
    if request.method == 'GET':
        return render_template('get_date_block.html', district=District, block=Block)
    else:
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']

        date = day+"_"+month+"_"+year

        return render_template('retired_on_date_block.html', date=date, district=District, block=Block)


@app.route('/raw_ttt_block/<string:month>/<string:year>/<string:District>/<string:Block>')
def ttw_this_month_block(month, year, District, Block):
    year10 = int(year) - 10
    year20 = int(year) - 20
    year30 = int(year) - 30

    year10 = str(year10)
    year20 = str(year20)
    year30 = str(year30)

    projects = Database.find("employees", {"$and": [{"$or": [
        {"$and": [{"Date of Joining": {'$regex': year10+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]},
        {"$and": [{"Date of Joining": {'$regex': year20+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]},
        {"$and": [{"Date of Joining": {'$regex': year30+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]}]},
        {"District": District},
        {"Block": Block}]})

    json_projects = []
    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/raw_ttt_panmp/<string:month>/<string:year>/<string:District>')
def ttw_this_month_panmp(month, year, District):
    year10 = int(year) - 10
    year20 = int(year) - 20
    year30 = int(year) - 30

    year10 = str(year10)
    year20 = str(year20)
    year30 = str(year30)

    projects = Database.find("employees", {"$and": [{"$or": [
        {"$and": [{"Date of Joining": {'$regex': year10+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]},
        {"$and": [{"Date of Joining": {'$regex': year20+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]},
        {"$and": [{"Date of Joining": {'$regex': year30+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]}
    ]}, {"District": District}]})

    json_projects = []
    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/raw_ttt/<string:month>/<string:year>')
def ttw_this_month(month, year):
    year10 = int(year) - 10
    year20 = int(year) - 20
    year30 = int(year) - 30

    year10 = str(year10)
    year20 = str(year20)
    year30 = str(year30)

    projects = Database.find("employees", {"$or": [
        {"$and": [{"Date of Joining": {'$regex': year10+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]},
        {"$and": [{"Date of Joining": {'$regex': year20+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]},
        {"$and": [{"Date of Joining": {'$regex': year30+'$'}}, {"Date of Joining": {'$regex': '^'+month}}]}
    ]})

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


@app.route('/get_tentwentythirty_panmp/<string:District>', methods=['POST', 'GET'])
def ttw_by_date_panmp(District):
    if request.method == 'GET':
        return render_template('get_month_date_panmp.html', district=District)
    else:
        month = request.form['month']
        year = request.form['year']

        return render_template('ttt_on_date_panmp.html', month=month, year=year, district=District)


@app.route('/get_tentwentythirty_block/<string:District>/<string:Block>', methods=['POST', 'GET'])
def ttw_by_date_block(District, Block):
    if request.method == 'GET':
        return render_template('get_month_date_block.html', district=District, block=Block)
    else:
        month = request.form['month']
        year = request.form['year']

        return render_template('ttt_on_date_block.html', month=month, year=year, district=District, block=Block)


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


@app.route('/sample_table_jaykumar')
def render_employees_sample():
        projects = Database.find("employees", {"$or": [{"nhis_id": ""},
                                                       {"nhis_id": " "}]})

        json_projects = []

        for project in projects:
            json_projects.append(project)

        df = pd.DataFrame(json_projects)

        df = df.groupby(['District']).size()

        all_employees_state = json.dumps(json_projects, default=json_util.default)

        return render_template('abcdef.html', dfLen=df)


@app.route('/employee_table/<string:_id>')
def render_individual_employees(_id):
    single_employee_array = []

    if Database.is_valid(_id):
        single_employee_dict = Database.find("employees", {'_id': ObjectId(_id)})
    else:
        single_employee_dict = Database.find("employees", {'_id': _id})

    for Emp in single_employee_dict:
        single_employee_array.append(Emp)

    single_employee_block = json.dumps(single_employee_array, default=json_util.default)

    return single_employee_block


@app.route('/block_table/<string:District>/<string:Block>')
def render_block_employees(District, Block):
    block_employees_array = []
    block_employees_dict = Database.find("employees", {"$and": [{'Block': Block},
                                                                {'District': District}]})

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
        if user.designation == "Admin":
            return render_template('profile_admin.html', user=user)

        else:
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
        if user.designation == "Admin":
            return render_template('profile_admin.html', user=user)
        else:
            return render_template('profile.html', user=user)


@app.route('/district_beneficiaries/<string:District>')
def all_district_employees(District):
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.designation == "PA NMP":
            return render_template('all_beneficiaries_PANMP.html', district=District)
        elif user.designation == "Admin":
            return render_template('all_beneficiaries_PANMP.html', district=District)
        else:
            return render_template('all_beneficiaries.html', district=District)
    else:
        return render_template('login_fail.html')


@app.route('/block_beneficiaries/<string:District>/<string:Block>')
@app.route('/block_beneficiaries')
def block_employees(District, Block):
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.designation == "PA NMP":
            return render_template('block_beneficiaries_panmp.html', block=Block, district=District)
        else:
            return render_template('block_beneficiaries.html', block=Block, district=District)
    else:
        return render_template('login_fail.html')


@app.route('/delete_employee/<string:_id>')
def delete_application(_id):

    Employee.deletefrom_mongo(_id=_id)

    return render_template('deleted.html')


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
        joiningDateCurrentPost = request.form['joiningDateCurrentPost']
        gender = request.form['gender']
        nhis = request.form['nhis']
        gpf = request.form['gpf']
        retirementDate = request.form['retirementDate']

        employee = Employee(district=district, name=name, block=block, panchayat=panchayat, center_name=center,
                            DOB=DOB, qualification=qualification, joining_date=joiningDate, designation=designation,
                            retirement_date=retirementDate, nhis_id=nhis, gpf=gpf,
                            joining_date_current_post=joiningDateCurrentPost, gender=gender)

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
        joiningDateCurrentPost = request.form['joiningDateCurrentPost']
        gender = request.form['gender']
        nhis = request.form['nhis']
        gpf = request.form['gpf']

        employee = Employee(district=district, name=name, block=block, panchayat=panchayat, center_name=center,
                            DOB=DOB, qualification=qualification, joining_date=joiningDate, designation=designation,
                            retirement_date=retirementDate, joining_date_current_post=joiningDateCurrentPost,
                            nhis_id=nhis, gender=gender, gpf=gpf)

        employee.update_employee(name=name, district=district, block=block, panchayat=panchayat,
                                 designation=designation, center_name=center, dob=DOB, doj=joiningDate,
                                 dor=retirementDate, emp_id=_id, joining_date_current_post=joiningDateCurrentPost,
                                 gender=gender, nhis_id=nhis, gpf=gpf)

        return render_template('beneficiary_added.html', employee=employee)


if __name__=='__main__':
    app.run(port=4095, debug=True)

