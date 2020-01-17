from odoo import http, exception, controller
from odoo.http import request
import werkzeug


class StockProductionLotController(http.Controller):
    
    @http.route("/api/stock_production_lot/<model('stock.production.lot'):lot>",
                cors='*',
                auth='token',
                methods=['PUT'],
                type='json'
                )
    def put_lot(self, lot):
        
        return {
            'lot': lot.id
        }

