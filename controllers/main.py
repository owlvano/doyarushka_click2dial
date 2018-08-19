
from odoo import http


class DoyarushkaClick2dialController(http.Controller):

    @http.route(
        '/doyarushka_click2dial/get_my_channel',
        type='json', auth='public')
    def get_my_channel(self, **kw):
        # my_channel = http.request.env['asterisk.server'].get_my_channel()
        # return my_channel
        true_val = http.request.env['asterisk.server'].get_my_channel_true()
        return true_val