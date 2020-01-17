from odoo import http, exceptions, models
from odoo.http import request
import werkzeug


class StockProductionLotController(http.Controller):

    @http.route("/api/stock_production_lot",
                cors='*',
                auth='token',
                methods=['PUT'],
                type='json'
                )
    def put_lot(self):
        return {
            'lot': 'lot.id'
        }
