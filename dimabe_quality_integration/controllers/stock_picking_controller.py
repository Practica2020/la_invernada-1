from odoo import http, exceptions
from odoo.http import request


class StockPickingController(http.Controller):

    @http.route('/api/stock_picking', type='json', methods=['GET'], auth='token', cors='*')
    def get_stock_picking(self):
        res = request.env['stock.picking'].search([('name', '=', 1)])
        if res:
            return res
        else:
            raise exceptions.ValidationError('lote no encontrado')
