from flask import Flask, render_template, url_for, redirect, session
from flask.globals import request
import csv, os

app = Flask(__name__)
app.secret_key = "SECRETRANDOM"

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/logged')
def basiclogged():
    username = session.get('username')
    with open("users.csv") as inp:
        for row in csv.DictReader(inp, fieldnames=["username", "recipes"]):
            if row["username"] == username:
                return render_template("logged.html", username=username, recipes=row["recipes"].split("|"))

@app.route('/logged', methods=['POST'])
def logged():
    username = request.form['username']
    session['username'] = username
    with open("users.csv") as inp:
        for row in csv.DictReader(inp, fieldnames=["username", "recipes"]):
            if row["username"] == username:
                return render_template("logged.html", username=username, recipes=row["recipes"].split("|"))
    with open("users.csv") as inp, open("tmp_users.csv", "w") as out:
        writer = csv.DictWriter(out, fieldnames=["user", "recipes"])
        for row in csv.DictReader(inp, fieldnames=["user", "recipes"]):
            if row != "":
                writer.writerow(row)
        writer.writerow({"user": username, "recipes": ""})
    os.remove("users.csv")
    os.rename("tmp_users.csv", "users.csv")
    return render_template("logged.html", username=username, recipes="No")

@app.route('/lognew')
def lognew():
    return render_template("lognew.html")

@app.route('/addnew', methods=['POST'])
def addnew():
    username = session.get('username')
    recipename = request.form['name']
    with open('users.csv') as inp, open('tmp_users.csv', 'w') as out:
        writer = csv.DictWriter(out, fieldnames=['username', 'recipes'])
        for row in csv.DictReader(inp, fieldnames=['username', 'recipes']):
            if row["username"] == username:
                allrecipes = row["recipes"].split("|")
                allrecipes.append(recipename)
                writer.writerow({"username": username, "recipes": '|'.join(allrecipes)})
            else:
                writer.writerow(row)
    os.remove("users.csv")
    os.rename("tmp_users.csv", "users.csv")
    return redirect(url_for("logged"))

if __name__ == "__main__":
    app.run()