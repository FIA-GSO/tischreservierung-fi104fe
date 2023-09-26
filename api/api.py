import datetime
from functools import wraps

import jwt

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'd0b817746d550d3ab4d275545fdaa53c'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123Meins'
app.config['MYSQL_DB'] = 'tischreservierung'
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

mysql = MySQL(app)

def authGuard(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'success': False})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'success': False})
        return f(data, *args, **kwargs)
    return decorator

def createToken(user):
    token = jwt.encode({'uId': user['id'],'role': user['role'],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
    return token

@app.route('/', methods=['GET'])
def home():
    return "<h1>Tischreservierung</h1>"


@app.route('/table', methods=['GET'])
def getTable():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM table''')
    dataDb = cursor.fetchall()
    cursor.close()
    return make_response(str(dataDb), )

app.run()