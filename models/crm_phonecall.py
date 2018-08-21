# -*- coding: utf-8 -*-
# © 2012-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons.base_phone.fields import Phone
from pprint import pformat
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class CrmPhonecall(models.Model):

    _inherit = 'crm.phonecall'
    _order = "id desc"
    
    support_ticket_id = fields.Many2one('website.support.ticket', "Ticket ID")
    voice_record_filename = fields.Char(string="Voice Record File Name")
    bridge_id = fields.Char(string="Unique Call Bridge ID", default=None)

    @api.model
    def create(self, values):
    	record = super(CrmPhonecall, self).create(values)

    	record.date = values['date']
    	record.name = values['name']
    	record.partner_id = values['partner_id']
    	record.direction = values['direction']    	
        record.user_id = values['user_id']
        record.state = values['state']

    	return record

    def set_bridge_id(self, bridge_id):
        self.bridge_id = bridge_id

    def create_phonecall_by_channel(self, user, chan):
        # check if record with this channel's bridge already exists
        new_bridge_id = chan.get('BridgeID')
        if self.search_count(['bridge_id', '=', new_bridge_id]) > 0:
            _logger.debug("FAILURE: Record with BridgeID '%s' already exists", new_bridge_id)
            return False

    	new_partner_id = None
        _logger.debug("Creating a phonecall by channel: ")
        _logger.debug(pformat(chan))
        phone_number = chan.get('CallerIDNum')
    	record = self.env['phone.common'].get_record_from_phone_number(phone_number)

        if record == False:
            _logger.debug("WARNING: No matching record with phonenumber '%s' was found", phone_number)
    	elif record[0] == 'res.partner':
            _logger.debug("SUCCESS: res.partner record with phonenumber '%s' was found", phone_number)
            new_partner_id = record[1]

    	values = {
    		'date': datetime.now(), 
    		'name': "Template name", 
    		'partner_id': new_partner_id,
    		'direction': self.determine_channel_direction(chan),
            'user_id': user,
            'state': 'done'}

    	new_phonecall_record = self.create(values)
        new_phonecall_record.set_bridge_id(new_bridge_id)

        _logger.debug("SUCCESS: New record of the model 'crm.phonecall' with name '%s' was created", new_phonecall_record.name)
        return new_phonecall_record

    # Very stupid determination mechanism based on Asterisk channel data output
    def determine_channel_direction(self, chan):
    	if chan.get('LinkedID') == chan.get('UniqueID'):
    		return 'outbound'
    	else:
    		return 'inbound'