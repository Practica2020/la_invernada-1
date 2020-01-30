from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock = fields.Many2one("stock.production.lot")

    product_qty = fields.Integer(rel="stock.product_qty")

    stock_id = fields.One2many(related="stock.stock_production_lot_serial_ids")

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
