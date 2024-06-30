import logging
import os
import datetime
import yaml
from flask import Flask, render_template, redirect, request, url_for, session
from views.ldap3_auth import get_ldap_info
from decorators.check_user import login_required

project_dir = os.getcwd()
MOUNTPOINT_PREFIX = os.environ.get("MOUNTPOINT_PREFIX", project_dir)
with open(os.path.join(MOUNTPOINT_PREFIX, 'common_settings.yml'), 'r') as f:
    local_settings = yaml.safe_load(f)

log_date = datetime.datetime.now()
filelog = logging.FileHandler((f'{project_dir}/logs/project_' + log_date.strftime('%Y_%m_%d') + '.log'))
consol_out = logging.StreamHandler()
logging.basicConfig(handlers=(filelog, consol_out),
                    level=logging.DEBUG,
                    format=u'%(asctime)s %(levelname)-3s: %(module)s.%(funcName)s +%(lineno)s %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) >= 8 and len(password) >= 8:
            ldap3_answer = get_ldap_info(
                username=username,
                password=password,
                ldap3_type='',
                client_ue=''
            )
            if ldap3_answer:
                try:
                    session['firstname_user'] = ldap3_answer['personal_info']['first_name']
                    session['lastname_user'] = ldap3_answer['personal_info']['last_name']
                    session['login_user'] = ldap3_answer['personal_info']['EmployeeID']
                    session['employees'] = ldap3_answer['employees']
                    session['EmployeeID'] = ldap3_answer['personal_info']['EmployeeID']
                    return redirect(url_for('dashboard'))
                except Exception as e:
                    logging.error(e)
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard/index.html', user=session['firstname_user'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=8000)
