
from odoo import http
import logging
_logger = logging.getLogger(__name__)

class DoyarushkaClick2dialController(http.Controller):


    @http.route(
        '/doyarushka_click2dial/create_phonecall_from_my_channel',
        type='json', auth='public')
    def create_phonecall_from_my_channel(self, **kw):
        
        # Check if the current user has rights to execute the method
        user = http.request.env.context.get('uid')
        if not user.context_auto_creation_crm_call:
        	return -1
        
    	my_channel = http.request.env['asterisk.server'].get_my_channel()
    	if not my_channel:
    		# Asterisk connection failed
    		return False
    	
    	new_phonecall = http.request.env['crm.phonecall'].create_phonecall_by_channel(my_channel)
    	if not new_phonecall:
    		return -2
    	
    	# TBD: Add response data json.dumps(response)
    	return True
