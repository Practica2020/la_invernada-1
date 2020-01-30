from odoo import fields, models, api
import logging


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    

#    stock_lots_id = fields.One2many(
#        related="stock_lots.stock_production_lot_serial_ids")

    product_lots = fields.Many2one("stock.production.lot",
        compute="filter_lots"
    )

    @api.onchange("product_id")
    def filter_lots(self):
        stock_lots = fields.Many2one("stock.production.lot")
       

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
