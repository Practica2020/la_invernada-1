from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stock_move_line_lot_ids = fields.One2many(
        string='Detalle',
        compute= '_compute_get_mp_move_line'
    )

    def _compute_get_mp_move_line(self):
        if self.get_mp_move():
            self.stock_move_line_lot_ids = self.get_mp_move().move_line_ids
