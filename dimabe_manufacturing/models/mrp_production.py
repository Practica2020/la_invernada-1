from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock = fields.Many2one("stock.production.lot",domain=[(product_id,'=',stock.product_id)])

    product_qty = fields.Float(rel="stock.product_qty")

    stock_id = fields.Char(rel="stock.stock_product_lot_id",compute="get_data_of_lot")

    @api.multi
    def get_data_of_lot(self):
        for item in self:
            if item.product_id:
                models._logger.error('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa {}'.format(self.stock))

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
