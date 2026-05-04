from flask import Flask, render_template, request, jsonify, redirect, url_for
from entities.user import User
from entities.account import Account
from entities.transaction import Transaction
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from entities.log import Log
from enums.log_type import LogType
from enums.profile import Profile
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/welcome')
@login_required
def welcome():
    print("USER ID:", current_user.id, type(current_user.id))

    account = Account.get_account_by_id(int(current_user.id))
    print("ACCOUNT:", account)

    transactions = []
    if account:
        print("ACCOUNT ID:", account.id)
        transactions = Transaction.get_transactions_by_account(account.id)
        print("TRANSACTIONS:", transactions)
        balance = Transaction.get_balance_by_account(account.id)

    return render_template("welcome.html", account=account, transactions=transactions, balance=balance)

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo electrónico ingresado ya se encuentra registrado."}), 409

    if User.save(name, email, password):
        return jsonify({"success": True, "message": "Su cuenta fue creada correctamente."}), 201
    else:
        return jsonify({"success": False, "message": "Ocurrió un error al crear su cuenta. Intente de nuevo"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)

    if user == "inactive":
        return jsonify({
            "success": False,
            "message": "Tu cuenta está inactiva."
        }), 403
    
    if user:

        login_user(user)
        #Invocar al metodo save de log
        Log.save(
            LogType.LOGIN,
            f"Login del usuario {user.email}",
            user
        )
        return jsonify({
            "success": True,
            "message": "Sesión inisciada correctamente"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Los datos de acceso ingresados no son correctos."
        }), 401
    
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/logs')
@login_required
def logs():
    if current_user.profile != Profile.ADMIN:
        return redirect(url_for('welcome'))
    
    all_logs = Log.get_all()
    return render_template('logs.html', logs=all_logs)

if __name__ == '__main__':
    app.run()