# from flask import Blueprint, render_template, abort, flash, redirect, url_for
# from flask_login import login_required, current_user

# admin_bp = Blueprint("admin_bp", __name__)

# @admin_bp.route("/admin")
# @login_required
# def admin():
#     if current_user.is_anonymous:
#         abort(403)
    
#     if current_user.role != 'admin':
#         flash('You have No access right to the Admin content.')
#         return redirect(url_for("main_bp.index"))
        
#     return render_template("admin/admin.html")
from flask import request, redirect, url_for, abort
from flask_admin import Admin
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from ..models import db, User, Post, Category, ApiToken

'''
class ForAdminModelView(ModelView):
    can_delete = False  # disable model deletion
    can_create = False
    can_edit = False

    page_size = 50  # the number of entries to display on the list view
    column_exclude_list = ['password', ] # Removing columns from the list view

    column_searchable_list = ['name', 'email']
    column_filters = ['country']
    # restrict the possible values for a text-field by specifying a list of select choices
    form_choices = {
                    'title': [
                        ('MR', 'Mr'),
                        ('MRS', 'Mrs'),
                        ('MS', 'Ms'),
                        ('DR', 'Dr'),
                        ('PROF', 'Prof.')
                    ]
                }
    # specify arguments to the WTForms widgets used to render those fields:
    form_args = {
                'name': {
                    'label': 'First Name',
                    'validators': [required()]
                }
            }
    #When your forms contain foreign keys, have those related models loaded via ajax, using:
    form_ajax_refs = {
                'user': {
                    'fields': ['first_name', 'last_name', 'email'],
                    'page_size': 10
                }
            }
    can_export = True #csv

    # Enabling CSRF Protection
    from flask_admin.form import SecureForm
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth_bp.login', next=request.url))

class ForStuffModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "stuff"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth_bp.login', next=request.url))
'''
class BaseAccessControl(ModelView):
    form_base_class = SecureForm
    page_size = 20

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role in ["stuff", "admin"]

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main_bp.login', next=request.url))


class UserAccessControl(BaseAccessControl):
    column_exclude_list = ['password_hash', ]
    column_searchable_list = ['name', 'email']
    column_filters = ['last_seen']
    can_create = False

class ApiTokenAccessControl(BaseAccessControl):
    column_filters = ['exipred']
    

admin = Admin(name="Admin Page", template_mode='bootstrap3')

admin.add_views(
            UserAccessControl(User, db.session),
            BaseAccessControl(Post, db.session),
            BaseAccessControl(Category, db.session),
            ApiTokenAccessControl(ApiToken, db.session)
        )

