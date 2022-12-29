from functools import wraps
from flask import session, redirect, flash


def login_required(ruta):
    @wraps(ruta)
    def wrapper(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            flash('Usted no tiene acceso a esta parte del sitio', 'error')
            return redirect('/')
        resp = ruta(*args, **kwargs)
        return resp
    
    return wrapper