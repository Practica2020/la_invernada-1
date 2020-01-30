from odoo import fields, models, api
import logging

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    lots = fields.Many2one("mrp.production.stock_lots")
    
    lots_id = fields.Integer(rel="lots.id")

    count_stock_production_lot_serial = fields.Integer(
        'Total Bultos',
        compute='_compute_count_stock_production_lot_serial'
    )

    @api.multi
    def _compute_count_stock_production_lot_serial(self):
        for item in self:
            models._logger.error(self.lots_id)
            if item.lot_id:
                item.count_stock_production_lot_serial = len(item.lot_id.stock_production_lot_serial_ids)
