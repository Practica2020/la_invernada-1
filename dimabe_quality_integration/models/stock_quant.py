from odoo import fields, models, api


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

    @api.onchange('balance')
    def onchange_balance(self):
        raise models.ValidationError('lal')
        for item in self:
            if item.lot_id and item.location_id.name == 'Stock':
                item.lot_id.stock_quant_balance = item.balance

