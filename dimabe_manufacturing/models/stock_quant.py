from odoo import api, models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    balance = fields.Float(
        'Saldo',
        compute='_compute_balance',
        store=True
    )

    @api.multi
    @api.depends('quantity', 'reserved_quantity')
    def _compute_balance(self):
        for item in self:
            item.balance = item.quantity - item.reserved_quantity
