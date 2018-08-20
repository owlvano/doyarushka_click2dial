# -*- coding: utf-8 -*-
# © 2012-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons.base_phone.fields import Phone
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class CrmPhonecall(models.Model):

    _inherit = 'crm.phonecall'
    _order = "id desc"
    
    support_ticket_id = fields.Many2one('website.support.ticket', "Ticket ID")
    voice_record_filename = fields.Char(string="Voice Record File Name")
    bridge_id = fields.Char(string="Unique Call Bridge ID")

    @api.model
    def create(self, values):
    	record = super(CrmPhonecall, self).create(values)

    	record.date = values['date'];
    	record.name = values['name'];
    	record.partner_id = values['partner_id'];
    	record.direction = values['direction'];
    	record.bridge_id = values['bridge_id'];

    	return record

    def create_phonecall_by_channel(self, chan):
    	new_partner_id = None

    	partner_record = self.env['phone.common'].get_record_from_phone_number(
                chan.get('CallerIDNum'))
    	if partner_record[0] == 'res.partner':
    		new_partner_id = partner_record[1]

    	values = {
    		'date': datetime.now(), 
    		'name': "Template name", 
    		'partner_id': new_partner_id,
    		'direction': self.determine_channel_direction(chan),
    		'bridge_id': chan.get('BridgeID')}
    	self.create(values)

    def determine_channel_direction(self, chan):
    	if chan.get('Data') == "Outgoing Line":
    		return 'outbound'
    	else:
    		return 'inbound'