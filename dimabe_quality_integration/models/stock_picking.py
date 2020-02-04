from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stock_move_line_lot_ids = fields.One2many(
        'stock.move.line',
        string='Detalle',
        compute='_compute_stock_move_line_lot_ids'
    )

    def _compute_stock_move_line_lot_ids(self):
        if self.get_mp_move():
            self.stock_move_line_lot_ids = self.get_mp_move().move_line_ids
