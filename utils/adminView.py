from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    can_create = False
    column_exclude_list = ['hashed_password', ]
    # create_modal = True
    edit_modal = True
    # edit_modal_template = 'admin/user_edit.html'


class ActionView(ModelView):
    can_create = False
    can_edit = False
