from odoo import http, exceptions
from odoo.http import request
import werkzeug


class StockPickingController(http.Controller):

    @http.route('/api/stock_picking', type='json', methods=['GET'], auth='token', cors='*')
    def get_stock_picking(self, lot):
        res = request.env['stock.picking'].search([('name', '=', lot)])
        if res:
            return {
                'ProducerCode': res.partner_id.id,
                'ProducerName': res.partner_id.name,
                'VarietyName': res.get_mp_move().product_id.get_variety(),
                'LotNumber': res.name,
                'DispatchGuideNumber': res.guide_number,
                'ReceptionDate': res.scheduled_date,
                'ReceptionKgs': res.net_weight,
                'ContainerType': res.get_canning_move().product_id.name,
                'Season': res.scheduled_date.year,
                'tare': res.tare_weight,
                'Warehouse': res.location_dest_id.name,
                'QualityWeight': res.quality_weight,
                'ContainerQuantity': res.get_canning_move().quantity_done,
                'ArticleDescription': res.get_mp_move().product_id.display_name
            }
        else:
            raise werkzeug.exceptions.NotFound('lote no encontrado')
