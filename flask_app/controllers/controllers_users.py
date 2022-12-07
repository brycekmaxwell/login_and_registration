from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.models_users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return render_template("log_in.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate(request.form):
        return redirect("/")
    data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    session["user_id"] = id

    return redirect("/dashboard")

@app.route("/log_in", methods=["POST"])
def login():
    users=User.get_by_email(request.form)

    if not users:
        flash("Invalid Email","login")
        return redirect("/")
    if not bcrypt.check_password_hash(users.password, request.form["password"]):
        flash("Invalid Password", "login")
        return redirect("/")
    session["users_id"]=users.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "users_id" not in session: 
        return redirect("/logout")
    data ={
        "id" : session["users_id"]
    }
    return render_template("sign_out.html", users=User.get_by_id(data))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")