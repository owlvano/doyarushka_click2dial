# -*- coding: utf-8 -*-
from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    # Field name starts with 'context_' to allow modification by the user
    # in his preferences, cf odoo/odoo/addons/base/res/res_users.py
    # in "def write()" of "class res_users(osv.osv)"
    context_auto_creation_crm_call = fields.Boolean(
	    string='Automatically create a call in CRM after a click2dial',
	    default=True)
