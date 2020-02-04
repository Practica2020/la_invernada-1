from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stock_move_line_lot_ids = fields.One2many(
        related='move_ids_without_package',
        string='Detalle'
    )
