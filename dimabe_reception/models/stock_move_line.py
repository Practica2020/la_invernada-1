from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def create(self, values_list):
        res = super(StockMoveLine, self).create(values_list)

        if res.move_id.picking_id and res.move_id.picking_id.picking_type_code == 'incoming':
            prefix = ''
            if res.move_id.product_id.categ_id.is_canning:
                prefix = 'ENV'
            res.lot_name = '{}{}'.format(prefix, res.move_id.picking_id.name)
            res.qty_done = res.product_uom_qty

        return res
