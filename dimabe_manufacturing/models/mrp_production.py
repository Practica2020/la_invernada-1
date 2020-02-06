from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock_lots = fields.Many2one("stock.production.lot")

    product_lot = fields.Many2one(rel="stock_lots.product_id")

    requested_qty = fields.Float('Cantidad Solicitada')

    serial_lot_ids = fields.One2many(related="stock_lots.stock_production_lot_serial_ids")

    potential_lot_ids = fields.One2many(
        'potential.lot',
        string='Posibles Lotes'
    )

    @api.model
    def get_potential_lot_ids(self):
        return self.env['stock.production.lot'].search([
            ('product_id', 'in', [self.product_id.id] + list(self.move_raw_ids.mapped('product_id.id'))),
            ('name', 'not in', list(self.potential_lot_ids.mapper('stock_production_lot_id.id'))),
            ('available_quantity', '>', 0)
        ])

    @api.multi
    def set_stock_move(self):
        product = self.env['stock.move'].create({'product_id': self.product_id})
        product_qty = self.env['stock.move'].create({'product_qty': self.product_qty})
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

    @api.model
    def create(self, values_list):
        res = super(MrpProduction, self).create(values_list)

        res.potential_lot_ids = self.get_potential_lot_ids()

        stock_picking = self.env['stock.picking'].search([
            ('name', '=', res.origin)
        ])

        if stock_picking:
            stock_picking.update({
                'has_mrp_production': True
            })

        return res
