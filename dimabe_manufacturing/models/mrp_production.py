from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock_lots = fields.Many2one(
        "stock.production.lot")
    
    serial_lot_ids = fields.One2many(related="stock_lots.stock_production_lot_serial_ids")

    # @api.onchange('product_id')
    # def onchange_stock_lots(self):
    #     if self.product_id:
    #         models._logger.error('product_id {}'.format(self.product_id))
    #         res = {}
    #         res['domain']={'stock_lots':["product_id","=",self.product_id]}
    #         return res

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
