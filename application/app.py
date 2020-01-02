import application
import jwt
import datetime
from flask import Flask,request
from application import routes,utils
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "thisisthesecretkey"

# JWT Initialization
jwt = JWTManager(app)
        
#Importing all the routes from a single file
routes.routes(app)


#for database connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
application.db = PyMongo(app)


# JWT authentication
@app.route('/auth',methods=['POST'])
def authenticate():
    try:
        email = request.get_json().get("email")
        password_res = application.db.db.users.distinct("password",{"email":email})[0]
    except Exception as e:
        email = 0
    
    try:
        password = request.get_json().get("password")
    except Exception as e:
        password = 0
    
    if email == 0 or password == 0:
        return utils.res({"status":"Fail","message":"email or password are blank!!!!!!"})
    elif check_password_hash(password_res,password):
        access_token = create_access_token(identity = email)
        refresh_token = create_refresh_token(identity = email)
        return utils.res({'message': 'Logged in as {}'.format(email),'access_token': access_token,'refresh_token': refresh_token})
    else:
        return utils.res({"status":"Fail","message":"email or password is Invalid"})


# Initializing Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5000', debug=True)