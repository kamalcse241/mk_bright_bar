import application
import flask
from application import user,user_expenses
from flask_jwt_extended import jwt_required, get_jwt_identity

### unproctetd api for test
def hello():
    return flask.Response('=============', 200)

################USERS########################
@jwt_required
def add_user():
    return user.add_user()

@jwt_required
def delete_user():
    return user.delete_user()

######################USER EXPENSES###########
@jwt_required
def list_expense(user_id):
    return user_expenses.list_expense(user_id)

@jwt_required
def list_all_users_expense():
    return user_expenses.list_all_users_expense()

@jwt_required
def add_expense():
    return user_expenses.add_expense()

@jwt_required    
def expense_edit(user_expense_id):
    return user_expenses.expense_edit(user_expense_id)

@jwt_required    
def expense_update(user_expense_id):
    return user_expenses.expense_update(user_expense_id)

@jwt_required    
def expense_delete():
    return user_expenses.delete_expense()

