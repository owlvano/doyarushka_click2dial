# -*- coding: utf-8 -*-
from odoo import api, fields, models

class WebsiteSupportTicket(models.Model):

    _inherit = "website.support.ticket"
    
    phonecall_ids = fields.One2many(
    	'crm.phonecall', 'support_ticket_id', string='Phone Calls')
    phonecall_count = fields.Integer(
        compute='_count_phonecalls', string='Number of Phonecalls',
        readonly=True)

    @api.multi
    @api.depends('phonecall_ids')
    def _count_phonecalls(self):
        cpo = self.env['crm.phonecall']
        for ticket in self:
            try:
                ticket.phonecall_count = cpo.search_count(
                    [('support_ticket_id', '=', ticket.id)])
            except:
                ticket.phonecall_count = 0