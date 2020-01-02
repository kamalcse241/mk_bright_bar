import application
from application import api


def routes(app):
    ### FOR TESTING
    app.add_url_rule('/meh', 'index', api.hello)
    
    ####USERS####
    app.add_url_rule('/user/add','Add User', api.add_user,methods=['POST'])
    app.add_url_rule('/user/delete','Delete User', api.delete_user,methods=['DELETE'])
    
    ####USER EXPENSES####
    app.add_url_rule('/user/expense/list/<int:user_id>','List User Expenses', api.list_expense)
    app.add_url_rule('/user/expense/list/all','List All User Expenses', api.list_all_users_expense)
    app.add_url_rule('/user/expense/add','Add User Expenses', api.add_expense,methods=['POST'])
    app.add_url_rule('/user/expense/edit/<int:user_expense_id>','Edit User Expenses', api.expense_edit)
    app.add_url_rule('/user/expense/update/<int:user_expense_id>','Update User Expenses', api.expense_update,methods=['PUT'])
    app.add_url_rule('/user/expense/delete','Delete User Expenses', api.expense_delete,methods=['DELETE'])
    