from odoo import http, exceptions
from odoo.http import request
import werkzeug
import json


class StockPickingController(http.Controller):

    @http.route('/api/stock_picking', type='json', methods=['GET'], auth='token', cors='*')
    def get_stock_picking(self, lot):
        res = request.env['stock.picking'].search([('name', '=', lot)])
        if res:
            return json.dumps(res)
        else:
            raise werkzeug.exceptions.NotFound()
