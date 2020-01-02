import application
import math
import decimal
import numpy
import json,datetime
from flask import Response, request
from bson import ObjectId
from datetime import time,timedelta,date,datetime

def res(data):
    rv = json.dumps(data,cls=DecimalEncoder, default=default)
    return Response(response=rv, status=200, mimetype="application/json")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        print("inside encoder")
        if isinstance(o, math.isnan()): return "NaN"
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

# Custom Datetime handler for JSONEncoder for int64
def default(o):
    if isinstance(o, numpy.int64): return int(o)
    if isinstance(o, ObjectId):
            return str(o)
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError

def autoIncrementId(collection):
    id_convn = collection.distinct("_id")
    if id_convn:
        res_id = int(sorted(id_convn)[-1]) + 1
    else:
        res_id = 1 
    return res_id

# conversion date to date object
def dateConvrsnToDateObject(my_date):
    try:
        year = int(my_date.split('/')[2])
        month = int(my_date.split('/')[1])
        day = int(my_date.split('/')[0])
        datetime_object = datetime(year, month, day)
    except Exception as e:
        datetime_object = datetime.combine(datetime.today(), time.min)
    
    return datetime_object
