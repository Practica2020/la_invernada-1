from odoo import fields, models, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    quality_analysis_id = fields.Many2one('quality.analysis', 'Análisis de Calidad')

    stock_quant_balance = fields.Float(
        compute='_compute_stock_quant_balance'
    )

    @api.multi
    def _compute_stock_quant_balance(self):
        for item in self:
            item.stock_quant_balance = item.quant_ids.filtered(lambda a: a.location_id.name == 'Stock').balance
