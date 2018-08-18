
from odoo import http


class AsteriskClick2dialController(http.Controller):

    @http.route(
        '/asterisk_click2dial/get_my_channel/',
        type='json', auth='public')
    def get_record_my_channel(self, **kw):
        my_channel = http.request.env['asterisk.server'].get_my_channel()
        return my_channel
