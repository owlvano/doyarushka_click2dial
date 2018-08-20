
from odoo import http
import logging
_logger = logging.getLogger(__name__)

class DoyarushkaClick2dialController(http.Controller):


    @http.route(
        '/doyarushka_click2dial/create_phonecall_from_my_channel',
        type='json', auth='public')
    def create_phonecall_from_my_channel(self, **kw):
        
        # Check if the current user has rights to execute the method

        # has_rights = http.request.env['res.users'].get_current_user_context_auto_creation_crm_call()
        current_user = http.request.env.user
        if not current_user.context_auto_creation_crm_call:
        	_logger.debug("FAILURE - Current user '%s' doesn't have rights to autocreate a call", current_user.name)
        	return -1
        _logger.debug("SUCCESS - Current user '%s' has rights to autocreate a call", current_user.name)

        # Commented for mock purposes
        # my_channel = http.request.env['asterisk.server'].get_mock_channel()
    	my_channel = http.request.env['asterisk.server'].get_my_channel()
    	if not my_channel:
    		# Asterisk connection failed
    		return False
    	

    	new_phonecall = http.request.env['crm.phonecall'].create_phonecall_by_channel(current_user, my_channel)
    	if not new_phonecall:
            # Record already exists
            return -2

    	
    	# # TBD: Add response data json.dumps(response)
    	return True
