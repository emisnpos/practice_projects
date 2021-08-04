from flask import Flask,\
    render_template, session, request, redirect, url_for
import dataMGMT
import os


app = Flask(__name__)

app.secret_key = os.urandom(12)

@app.route("/")
@app.route("/index")
def main():
    return render_template("index.html")


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        dataMGMT.insert_username_userpassword(username, password)
        return redirect(url_for('main'))
    return render_template("registration.html")


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        hashed_password = dataMGMT.valid_password(username)['password']
        if dataMGMT.verify_password(password, hashed_password):
            session['username'] = username
            session['logged_in'] = True
            return redirect('/')
    return render_template("login.html")


@app.route("/logout", methods=['GET', 'POST'])
def log_out():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(
        debug=True)
