from flask import request
import application
import requests
import json
from application import utils
from datetime import time,timedelta,date,datetime

def list_expense(user_id):
    collection = application.db.db.user_expense
    cursor = collection.aggregate([{"$match":{"user_id": user_id}}])
    final_data = [ document for document in cursor ]
    return utils.res(final_data)

def list_all_users_expense():
    collection = application.db.db.user_expense
    projection = {"_id":1,"user_id":1,"cost":1,"date":1,"item":1,"user_name":"$user_details.name","user_email":"$user_details.email"}
    cursor = collection.aggregate([{"$lookup":{"from":"users","localField":"user_id","foreignField":"_id","as":"user_details"}},{"$project":projection}])
    final_data = [ document for document in cursor ]
    return utils.res(final_data)

def add_expense():
    response = {}
    result = {}
    collection = application.db.db.user_expense
    try:
        response["user_id"] = int(request.get_json().get("user_id")) if not request.get_json().get("user_id") == "" else 0
    except Exception as e:
        response["user_id"] = 0

    try:
    	response["cost"] = float(request.get_json().get("cost")) if not request.get_json().get("cost") == "" else 0
    except Exception as e:
    	response["cost"] = 0
    
    try:
    	response["item"] = request.get_json().get("item") if not request.get_json().get("item") == "" else 0
    except Exception as e:
    	response["item"] = 0
    
    try:
        ## input date must be in the format of dd/mm/yyyy
    	response["date"] = utils.dateConvrsnToDateObject(request.get_json().get("date")) if not request.get_json().get("date") == "" else datetime.combine(datetime.today(), time.min)
    except Exception as e:
        response["date"] = datetime.combine(datetime.today(), time.min)

    ## we need _id in normal number not ObjectID format
    response["_id"] = utils.autoIncrementId(collection)

    if response["user_id"]==0:
        result["message"] = "Please Enter Valid UserId"
        result["status"] = "Fail"
    elif response["cost"]==0:
        result["message"] = "Please Enter Valid Cost"
        result["status"] = "Fail"
    elif response["item"]==0:
        result["message"] = "Please Enter Item"
        result["status"] = "Fail"
    else:
        collection.insert(response)
        result["message"] = "User Added Successfully!!!!! "
        result["status"] = "Success"

    return utils.res(result)

def expense_edit(user_expense_id):
    cursor = collection.find({"_id":user_expense_id})
    final_data = [ document for document in cursor ]
    return utils.res(final_data)

def expense_update(user_expense_id):
    response = {}
    result = {}
    # collection = application.db.db.user_expense
    try:
        response["user_id"] = int(request.get_json().get("user_id")) if not request.get_json().get("user_id") == "" else 0
    except Exception as e:
        response["user_id"] = 0

    try:
        response["cost"] = float(request.get_json().get("cost")) if not request.get_json().get("cost") == "" else 0
    except Exception as e:
        response["cost"] = 0
    
    try:
        response["item"] = request.get_json().get("item") if not request.get_json().get("item") == "" else 0
    except Exception as e:
        response["item"] = 0

    response["_id"] = user_expense_id
    
    try:
        ## input date must be in the format of dd/mm/yyyy
        response["date"] = utils.dateConvrsnToDateObject(request.get_json().get("date")) if not request.get_json().get("date") == "" else datetime.combine(datetime.today(), time.min)
    except Exception as e:
        response["date"] = datetime.combine(datetime.today(), time.min)

    if response["user_id"]==0:
        result["message"] = "Please Enter Valid UserId"
        result["status"] = "Fail"
    elif response["cost"]==0:
        result["message"] = "Please Enter Valid Cost"
        result["status"] = "Fail"
    elif response["item"]==0:
        result["message"] = "Please Enter Item"
        result["status"] = "Fail"
    else:
        res = collection.update({"_id":response["_id"]},response,upsert=True)
        print(res)
        result["message"] = "User Updated Successfully!!!!! "
        result["status"] = "Success"

    return utils.res(result)
    
def delete_expense():
    result = {}
    try:
        user_expense_id = int(request.get_json().get("user_expense_id")) if not request.get_json().get("user_expense_id") == "" else 0
    except Exception as e:
        user_expense_id = 0

    if user_expense_id == 0:
        return utils.res({"message":"User Expense Id Invalid","status":"fail"})

    # collection = application.db.db.user_expense
    if collection.find({'_id': user_expense_id}).count() > 0:
        response = collection.delete_one({"_id":user_expense_id})
        result["message"] = "Deleted successfully"
        result["status"] = "Success"
    else:
        result["message"] = "No Such Record Found"
        result["status"] = "fail"
    return utils.res(result)

