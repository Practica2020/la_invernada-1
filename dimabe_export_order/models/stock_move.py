from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    reserved_amount = fields.Float(
        'total',
        compute='_compute_reserved_amount'
    )

    @api.model
    def _compute_reserved_amount(self):
        self.reserved_amount = 100

