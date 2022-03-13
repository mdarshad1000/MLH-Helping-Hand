import pyrebase
from flask import *
import pickle
import numpy as np
from ml_model.model import training_scaler

model = pickle.load(open('model.pkl','rb'))

scaler = training_scaler()

app = Flask(__name__)
config = {
    "apiKey": "AIzaSyBs27uES8ItnzIdLKfcPRceB8cZxE2LyW8",
    "authDomain": "helpinghand-290e9.firebaseapp.com",
    "databaseURL": "https://helpinghand-290e9.firebaseio.com",
    "projectId": "helpinghand-290e9",
    "storageBucket": "helpinghand-290e9.appspot.com",
    "messagingSenderId": "273535791016",
    "appId": "1:273535791016:web:3755fc4ba69a3e6673379d",
    "measurementId": "G-H7QW7W9BL8"
}

# INITIALIZE FIREBASE
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email=person["email"], name=person["name"])
    else:
        return redirect(url_for('login'))


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            return redirect(url_for('welcome'))
        except:
            return redirect(url_for('result'))
    else:
        if person["is_logged_in"] == True:
            if request.method == 'POST':
                if request.form.get('logout') == 'LOGOUT':
                    auth.signOut()
                    return redirect(url_for('login'))
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('result'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            return redirect(url_for('welcome'))
        except:
            return redirect(url_for('register'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))


@app.route('/restroml', methods=['GET', 'POST'])
def restroml():
    if request.method == "POST":
        ml = request.form
        veg_qty = ml["vegquantity"]
        nonveg_qty = ml["nonvegquantity"]
        people = ml["people"]
        pass
    
    int_features=[int(veg_qty), int(nonveg_qty), int(people)]
    user_data = np.array(int_features).reshape((1,-1))
    user_data_scaled = scaler.transform(user_data)
    
    prediction = model.predict(user_data_scaled)
    return prediction[0]



if __name__ == "__main__":
    app.run(debug=True)
