# -*- coding: utf-8 -*-
# © 2010-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from pprint import pformat
import logging
_logger = logging.getLogger(__name__)


class AsteriskServer(models.Model):
    '''Asterisk server object, stores the parameters of the Asterisk IPBXs'''
    _inherit = "asterisk.server"
    
    @api.model
    def _is_my_channel(self, chan, user):
        '''Method designed to be inherited to work with
        very old or very new versions of Asterisk'''
        sip_account = user.asterisk_chan_type + '/' + user.resource
        internal_number = user.internal_number
        # 4 = Ring
        # 6 = Up
        if (
                chan.get('ChannelState') in ('4', '6') and (
                    chan.get('ConnectedLineNum') == internal_number or
                    chan.get('EffectiveConnectedLineNum') == internal_number or
                    sip_account in chan.get('BridgedChannel', ''))):
            _logger.debug(
                "Found a matching Event with channelstate = %s",
                chan.get('ChannelState'))
            return True
        # Compatibility with Asterisk 1.4
        if (
                chan.get('State') == 'Up' and
                sip_account in chan.get('Link', '')):
            _logger.debug("Found a matching Event in 'Up' state")
            return True
        return False

    @api.model
    def _get_my_channel(self):
        user, ast_server, ast_manager = self._connect_to_asterisk()
        my_channel = False
        try:
            list_chan = ast_manager.Status()
            # from pprint import pprint
            # pprint(list_chan)
            _logger.debug("Result of Status AMI request:")
            _logger.debug(pformat(list_chan))
            for chan in list_chan.values():
                if self._is_my_channel(chan, user):
                    my_channel = chan
                    break
        except Exception, e:
            _logger.error(
                "Error in the Status request to Asterisk server %s",
                ast_server.ip_address)
            _logger.error(
                "Here are the details of the error: '%s'", unicode(e))
            raise UserError(
                _("Can't get channel data from Asterisk.\nHere is the "
                    "error: '%s'" % unicode(e)))

        finally:
            ast_manager.Logoff()

        _logger.debug("Fetching channel: '%s'", my_channel)
        return my_channel

    def _get_my_channel_true(self):
        _logger.debug("Found a matching Event in 'Up' state")
        return True