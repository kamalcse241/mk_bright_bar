import application
import json
from application import utils
from flask import request
from werkzeug.security import generate_password_hash

def add_user():
    response = {}
    collection = application.db.db.users
    result = {}

    try:
        response["name"] = request.get_json().get("name") if not request.get_json().get("name") == "" else 0
    except Exception as e:
        response["name"] = 0
    
    try:
        response["email"] = request.get_json().get("email") if not request.get_json().get("email") == "" else 0
    except Exception as e:
        response["email"] = 0
    
    try:
        response["password"] = generate_password_hash(request.get_json().get("password"), method='sha256') if not request.get_json().get("password") == "" else 0
    except Exception as e:
        response["password"] = 0
    
    try:
        response["mobile"] = int(request.get_json().get("mobile")) if not request.get_json().get("mobile") == "" else 0
    except Exception as e:
        response["mobile"] = 0

    #role_id 1 = Admin
    #role_id 2 = Super Admin
    try:
        response["role_id"] = int(request.get_json().get("role_id")) if not request.get_json().get("mobile") == "" else 2
    except Exception as e:
        response["role_id"] = 0

    ## we need _id in normal number not ObjectID format
    response["_id"] = utils.autoIncrementId(collection)

    ### checking if email already exist or not
    email_exist = collection.distinct("email",{"email":response["email"]})

    if response["name"] == 0 or response["password"] == 0 or response["email"] == 0 or response["role_id"] == 0:
        result["message"] = "Please Enter Name,Password,Email,Role"
        result["status"] = "Fail"
    elif email_exist:
        result["message"] = "Email Already Exits"
        result["status"] = "Fail"
    else:
        collection.insert(response)
        result["message"] = "User Added Successfully!!!!! "
        result["status"] = "Success"

    return utils.res(result)

def delete_user():
    result = {}
    try:
        user_id = int(request.get_json().get("user_id")) if not request.get_json().get("user_id") == "" else 0
    except Exception as e:
        user_id = 0

    if user_id == 0:
        return utils.res({"message":"User Id is Invalid","status":"fail"})

    collection = application.db.db.users
    if collection.find({'_id': user_id}).count() > 0:
        response = collection.delete_one({"_id":user_id})
        result["message"] = "Deleted successfully"
        result["status"] = "Success"
    else:
        result["message"] = "No Such Record Found"
        result["status"] = "fail"
    return utils.res(result)
