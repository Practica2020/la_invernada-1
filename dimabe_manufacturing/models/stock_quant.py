from odoo import api, models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    balance = fields.Float(
        'Saldo',
        compute='_compute_balance'
    )

    @api.multi
    def _compute_balance(self):
        for item in self:
            item.balance = item.quantity - item.reserved_quantity
