from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock_lots = fields.Many2one(
        "stock.production.lot")

    lot_id = fields.Char(rel="stock_lots.name")
    
    serial_lot_ids = fields.One2many(related="stock_lots.stock_production_lot_serial_ids",compute='_get_serial')

    @api.onchange('product_id')
    def _get_serial(self):
        if self.product_id:
            if self.product_id == self.stock_lots.product_id:
                models._logger.error('Esta')

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
