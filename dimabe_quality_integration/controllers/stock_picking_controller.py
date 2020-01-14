from odoo import http, exceptions
from odoo.http import request
import werkzeug
import json
from datetime import datetime


class StockPickingController(http.Controller):

    @http.route('/api/stock_picking', type='json', methods=['GET'], auth='token', cors='*')
    def get_stock_picking(self, lot):
        res = request.env['stock.picking'].search([('name', '=', lot)])
        if res:
            return {
                'ProducerCode': 0,
                'ProducerName': res.partner_id.name,
                'VarietyName': res.get_mp_move().product_id.name,
                'LotNumber': res.name,
                'DispatchGuideNumber': res.guide_number,
                'ReceptionDate': res.scheduled_date,
                'ReceptionKgs': '',
                'DryKgs': '',
                'Season': 0,
                'QualityNumber': '',
                'Warehouse': '',
                'QualityWeight': '',
                'ContainerQuantity': '',
                'ArticleDescription': res.get_mp_move().product_id.display_name,
                'QualityGreenId': ''
            }
        else:
            raise werkzeug.exceptions.NotFound('lote no encontrado')
