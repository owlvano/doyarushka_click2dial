# -*- coding: utf-8 -*-
# © 2012-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons.base_phone.fields import Phone


class CrmPhonecall(models.Model):

    _inherit = 'crm.phonecall'
    _order = "id desc"

    
    support_ticket_id = fields.Many2one('website.support.ticket', "Ticket ID")
    voice_record_filename = fields.Char(string="Voice Record File Name")