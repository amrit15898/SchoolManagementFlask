import functools
from flask import session, redirect

def auth(view_fun):
    @functools.wraps(view_fun)
    def decorated(*args, **kwargs):
        if "name" not in session:
            return redirect("/login-page")
        return view_fun(*args, **kwargs)
    return decorated

def guest(view_fun):
    @functools.wraps(view_fun)
    def decorated(*args, **kwargs):
        if "name" in session:
            return redirect("/dashboard")
        return view_fun(*args, **kwargs)
    return decorated