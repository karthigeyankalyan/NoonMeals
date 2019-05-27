from time import strftime

import pandas as pd

from src.common.database import Database
from src.models.employee import Employee
from flask import Flask, render_template, request, session, make_response
from datetime import datetime, date

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


@app.route('/get_all_retirements_within/<string:District>/<string:Block>', methods=['POST', 'GET'])
def enter_dates_to_get_retirements_within(District, Block):
    email = session['email']
    user = User.get_by_email(email)
    if request.method == 'GET':
        return render_template('get_retirement_date_within.html', district=District, block=Block)

    else:
        start_date = request.form['startDate']
        end_date = request.form['endDate']

        if user.designation == "Block Operator":
            return render_template('all_retirements_district.html', user=user, start_date=start_date,
                                   end_date=end_date, district=District, block=Block)
        elif user.designation == "Admin":
            return render_template('all_retirements_admin.html', user=user, start_date=start_date,
                                   end_date=end_date)
        else:
            return render_template('all_retirements_panmp.html', user=user, start_date=start_date,
                                   end_date=end_date, district=District, block=Block)


@app.route('/raw_retirements_within_date_district/<string:start_date>/<string:end_date>/'
           '<string:District>/<string:Block>')
def retirements_within_by_district(start_date, end_date, District, Block):
    all_transactions = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())

    all_trans_dict = Database.find("employees", {"$and": [{"Date of RetirementV2": {"$gte": start, "$lt": end}},
                                                          {"District": District},
                                                          {"Block": Block}]})

    for tran in all_trans_dict:
        all_transactions.append(tran)

    all_t = json.dumps(all_transactions, default=json_util.default)

    return all_t


@app.route('/raw_retirements_within_date_block_alone/<string:District>/<string:Block>')
def retirements_within_by_block_alone(District, Block):
    all_transactions = []

    end = datetime.now()

    all_trans_dict = Database.find("employees", {"$and": [{"Date of RetirementV2": {"$lt": end}},
                                                          {"District": District},
                                                          {"Block": Block}]})

    for tran in all_trans_dict:
        all_transactions.append(tran)

    all_t = json.dumps(all_transactions, default=json_util.default)

    return all_t


@app.route('/raw_retirements_within_date_panmp/<string:start_date>/<string:end_date>/'
           '<string:District>')
def retirements_within_by_panmp(start_date, end_date, District):
    all_transactions = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())

    all_trans_dict = Database.find("employees", {"$and": [{"Date of RetirementV2": {"$gte": start, "$lt": end}},
                                                          {"District": District}]})

    for tran in all_trans_dict:
        all_transactions.append(tran)

    all_t = json.dumps(all_transactions, default=json_util.default)

    return all_t


@app.route('/raw_retirements_within_date_overall/<string:start_date>/<string:end_date>')
def retirements_within_overall(start_date, end_date):
    all_transactions = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())

    all_trans_dict = Database.find("employees", {"Date of RetirementV2": {"$gte": start, "$lt": end}})

    for tran in all_trans_dict:
        all_transactions.append(tran)

    all_t = json.dumps(all_transactions, default=json_util.default)

    return all_t


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
def retirement_by_date_of_panmp(District):
    email = session['email']
    user = User.get_by_email(email)
    if request.method == 'GET':
        return render_template('get_month_date_panmp.html', district=District)

    else:
        start_date = request.form['startDate']
        end_date = request.form['endDate']

        return render_template('all_retirements_district.html', user=user, start_date=start_date,
                               end_date=end_date, district=District)


@app.route('/change_password/<string:_id>', methods=['POST', 'GET'])
def change_password(_id):
    user = User.get_by_id(int(_id))
    if request.method == 'GET':
        return render_template('update_password.html', user=user, user_id=_id)
    else:
        old_password = request.form['oldPassword']
        newPassword = request.form['newPassword']
        newPasswordAgain = request.form['newPasswordAgain']

    if user.password == old_password:
        if newPassword == newPasswordAgain:
            User.change_password(user_id=_id, new_password=newPassword)
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


@app.route('/raw_ttt_block/<string:start_date>/<string:end_date>/<string:District>/<string:Block>')
def ttw_this_month_block(start_date, end_date, District, Block):

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())

    ten_year_start_date = date(int(start.strftime('%Y'))-10, int(start.strftime('%m')), int(start.strftime('%d')))
    ten_year_end_date = date(int(end.strftime('%Y'))-10, int(end.strftime('%m')), int(end.strftime('%d')))

    twenty_year_start_date = date(int(start.strftime('%Y'))-20, int(start.strftime('%m')), int(start.strftime('%d')))
    twenty_year_end_date = date(int(end.strftime('%Y'))-20, int(end.strftime('%m')), int(end.strftime('%d')))

    thirty_year_start_date = date(int(start.strftime('%Y'))-30, int(start.strftime('%m')), int(start.strftime('%d')))
    thirty_year_end_date = date(int(end.strftime('%Y'))-30, int(end.strftime('%m')), int(end.strftime('%d')))

    ten_year_start_date = datetime.combine(ten_year_start_date, datetime.now().time())
    ten_year_end_date = datetime.combine(ten_year_end_date, datetime.now().time())
    twenty_year_start_date = datetime.combine(twenty_year_start_date, datetime.now().time())
    twenty_year_end_date = datetime.combine(twenty_year_end_date, datetime.now().time())
    thirty_year_start_date = datetime.combine(thirty_year_start_date, datetime.now().time())
    thirty_year_end_date = datetime.combine(thirty_year_end_date, datetime.now().time())

    projects = Database.find("employees", {"$and": [
        {"$or": [{"Date of JoiningV2": {"$gte": ten_year_start_date, "$lt": ten_year_end_date}},
                 {"Date of JoiningV2": {"$gte": twenty_year_start_date, "$lt": twenty_year_end_date}},
                 {"Date of JoiningV2": {"$gte": thirty_year_start_date, "$lt": thirty_year_end_date}}]},
        {"District": District},
        {"Block": Block}]})

    json_projects = []

    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/raw_ttt_panmp/<string:start_date>/<string:end_date>/<string:District>')
def ttw_this_month_panmp(start_date, end_date, District):

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())

    ten_year_start_date = date(int(start.strftime('%Y'))-10, int(start.strftime('%m')), int(start.strftime('%d')))
    ten_year_end_date = date(int(end.strftime('%Y'))-10, int(end.strftime('%m')), int(end.strftime('%d')))

    twenty_year_start_date = date(int(start.strftime('%Y'))-20, int(start.strftime('%m')), int(start.strftime('%d')))
    twenty_year_end_date = date(int(end.strftime('%Y'))-20, int(end.strftime('%m')), int(end.strftime('%d')))

    thirty_year_start_date = date(int(start.strftime('%Y'))-30, int(start.strftime('%m')), int(start.strftime('%d')))
    thirty_year_end_date = date(int(end.strftime('%Y'))-30, int(end.strftime('%m')), int(end.strftime('%d')))

    ten_year_start_date = datetime.combine(ten_year_start_date, datetime.now().time())
    ten_year_end_date = datetime.combine(ten_year_end_date, datetime.now().time())
    twenty_year_start_date = datetime.combine(twenty_year_start_date, datetime.now().time())
    twenty_year_end_date = datetime.combine(twenty_year_end_date, datetime.now().time())
    thirty_year_start_date = datetime.combine(thirty_year_start_date, datetime.now().time())
    thirty_year_end_date = datetime.combine(thirty_year_end_date, datetime.now().time())

    projects = Database.find("employees", {"$and": [
        {"$or": [{"Date of JoiningV2": {"$gte": ten_year_start_date, "$lt": ten_year_end_date}},
                 {"Date of JoiningV2": {"$gte": twenty_year_start_date, "$lt": twenty_year_end_date}},
                 {"Date of JoiningV2": {"$gte": thirty_year_start_date, "$lt": thirty_year_end_date}}]},
        {"District": District}]})

    json_projects = []

    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/raw_ttt/<string:start_date>/<string:end_date>')
def ttw_this_month(start_date, end_date):

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),
                             datetime.now().time())
    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),
                           datetime.now().time())

    ten_year_start_date = date(int(start.strftime('%Y'))-10, int(start.strftime('%m')), int(start.strftime('%d')))
    ten_year_end_date = date(int(end.strftime('%Y'))-10, int(end.strftime('%m')), int(end.strftime('%d')))

    twenty_year_start_date = date(int(start.strftime('%Y'))-20, int(start.strftime('%m')), int(start.strftime('%d')))
    twenty_year_end_date = date(int(end.strftime('%Y'))-20, int(end.strftime('%m')), int(end.strftime('%d')))

    thirty_year_start_date = date(int(start.strftime('%Y'))-30, int(start.strftime('%m')), int(start.strftime('%d')))
    thirty_year_end_date = date(int(end.strftime('%Y'))-30, int(end.strftime('%m')), int(end.strftime('%d')))

    ten_year_start_date = datetime.combine(ten_year_start_date, datetime.now().time())
    ten_year_end_date = datetime.combine(ten_year_end_date, datetime.now().time())
    twenty_year_start_date = datetime.combine(twenty_year_start_date, datetime.now().time())
    twenty_year_end_date = datetime.combine(twenty_year_end_date, datetime.now().time())
    thirty_year_start_date = datetime.combine(thirty_year_start_date, datetime.now().time())
    thirty_year_end_date = datetime.combine(thirty_year_end_date, datetime.now().time())

    projects = Database.find("employees", {"$or": [{"Date of JoiningV2": {"$gte": ten_year_start_date, "$lt": ten_year_end_date}},
                                                   {"Date of JoiningV2": {"$gte": twenty_year_start_date, "$lt": twenty_year_end_date}},
                                                   {"Date of JoiningV2": {"$gte": thirty_year_start_date, "$lt": thirty_year_end_date}}]})

    json_projects = []

    for project in projects:
        json_projects.append(project)
    all_employees_retiring = json.dumps(json_projects, default=json_util.default)

    return all_employees_retiring


@app.route('/get_tentwentythirty', methods=['POST', 'GET'])
def ttw_by_date():
    if request.method == 'GET':
        return render_template('get_month_date_overall.html')
    else:
        start_date = request.form['startDate']
        end_date = request.form['endDate']

        return render_template('ttt_on_date_overall.html', start_date=start_date, end_date=end_date)


@app.route('/get_tentwentythirty_panmp/<string:District>', methods=['POST', 'GET'])
def ttw_by_date_panmp(District):
    if request.method == 'GET':
        return render_template('get_month_date_district.html', district=District)
    else:
        start_date = request.form['startDate']
        end_date = request.form['endDate']

        return render_template('ttt_on_date_panmp.html', start_date=start_date, end_date=end_date,
                               district=District)


@app.route('/get_tentwentythirty_block/<string:District>/<string:Block>', methods=['POST', 'GET'])
def ttw_by_date_block(District, Block):
    if request.method == 'GET':
        return render_template('get_month_date_block.html', district=District, block=Block)
    else:
        start_date = request.form['startDate']
        end_date = request.form['endDate']

        return render_template('ttt_on_date_block.html', start_date=start_date, end_date=end_date,
                               district=District, block=Block)


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
        projects = Database.find("employees", {"$or": [{"gpf": ""},
                                                       {"gpf": " "}]})

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
        elif user.designation == "PA NMP":
            return render_template('profile_NMP.html', user=user)
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
        elif user.designation == "PA NMP":
            return render_template('profile_NMP.html', user=user)
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


@app.route('/retired_block_employees/<string:District>/<string:Block>')
def retired_employees_block_employees(District, Block):
    email = session['email']
    if email is not None:
        user = User.get_by_email(email)
        if user.designation == "PA NMP":
            return render_template('retired_block_employees.html', block=Block, district=District)
        else:
            return render_template('retired_block_employees.html', block=Block, district=District)
    else:
        return render_template('login_fail.html')


@app.route('/delete_employee/<string:_id>')
def delete_application(_id):

    Employee.deletefrom_mongo(_id=_id)

    return render_template('deleted.html')


@app.route('/retirement_employees')
def retired_employees():
    return render_template('retirement_employees.html')


@app.route('/new_employee/<string:_id>', methods=['POST', 'GET'])
def my_entries(_id):
    if request.method == 'GET':
        return render_template('form.html', _id=_id)
    else:
        email = session['email']
        user = User.get_by_email(email)
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
                            retirement_date=retirementDate, nhis_id=nhis, gpf=gpf, gender=gender,
                            joining_date_current_post=joiningDateCurrentPost)

        employee.save_to_mongo()

        return render_template('beneficiary_added.html', employee_id=employee._id, district=user.district,
                               block=user.block)


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
        joiningDate = request.form['joiningDate']
        designation = request.form['designation']
        retirementDate = request.form['retirementDate']
        joiningDateCurrentPost = request.form['joiningDateCurrentPost']
        gender = request.form['gender']
        nhis = request.form['nhis']
        gpf = request.form['gpf']
        qualification = request.form['qualification']
        MOA = request.form['MOA']
        community = request.form['community']
        strength = request.form['strength']

        user = User.get_by_email(session['email'])

        Employee.update_employee(name=name, district=district, block=block, panchayat=panchayat,
                                 designation=designation, center_name=center, dob=DOB, doj=joiningDate,
                                 dor=retirementDate, emp_id=_id, joining_date_current_post=joiningDateCurrentPost,
                                 gender=gender, nhis_id=nhis, gpf=gpf, qualification=qualification,
                                 strength=strength, moa=MOA, community=community)

        return render_template('beneficiary_added.html', employee_id=_id, district=user.district, block=user.block)


@app.route('/loggedOut')
def log_out():
    email = session['email']
    user = User.get_by_email(email)
    if email is not None:
        if user.society_name is not None:
            user.logout()
            return render_template('logged_out.html', user=user.username)

    else:
        return render_template('login_fail.html')


if __name__=='__main__':
    app.run(port=4095, debug=True)

