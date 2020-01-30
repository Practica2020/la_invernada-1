from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    test = fields.Many2one('stock.production.lot')

    t = fields.Many2one(rel="test.stock_production_lot_serial_ids")

    id = fields.Char(rel="t.stock_production_lot_id")

    lots = fields.Many2one(
        "stock.production.lots.stock_production_serial_ids", "Lotes")

    @api.model
    def _get_data_lots(self):
        for item in self.lots:
            if item.lot_id:
                models._logger.error(item)

    @api.multi
    def calculate_done(self):
        for item in self:
            for line_id in item.finished_move_line_ids:
                line_id.qty_done = line_id.lot_id.total_serial

    @api.multi
    def button_mark_done(self):
        self.calculate_done()
        return super(MrpProduction, self).button_mark_done()
