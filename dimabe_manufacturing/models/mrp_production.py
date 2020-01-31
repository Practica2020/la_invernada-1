from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock_lots = fields.Many2one(
        "stock.production.lot")

    serial_lot_ids = fields.One2many(related="stock_lots.stock_production_lot_serial_ids",compute='_get_serial')


    @api.multi
    def set_stock_move(self):
        product = self.env['stock.move'].create({'product_id':self.product_id})
        product_qty = self.env['stock.move'].create({'product_qty':self.product_qty})
        self.env.cr.commit()

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
