from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session['EmployeeID']
        except Exception:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
