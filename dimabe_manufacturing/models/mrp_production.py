from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock_lots = fields.Many2one("stock.production.lot")

    product_lot = fields.Many2one(
        'product.product',
        related="stock_lots.product_id"
    )

    requested_qty = fields.Float('Cantidad Solicitada')

    serial_lot_ids = fields.One2many(
        'stock.production.lot.serial',
        related="stock_lots.stock_production_lot_serial_ids"
    )

    potential_lot_ids = fields.One2many(
        'potential.lot',
        'mrp_production_id'
    )

    @api.model
    def get_potential_lot_ids(self):
        return [{
            'stock_production_lot_id': lot.id,
            'mrp_production_id': self.id,
            'lot_available-quantity': lot.stock_quant_balance
        } for lot in self.env['stock.production.lot'].search([
            ('product_id', 'in', list(self.move_raw_ids.mapped('product_id.id'))),
            ('name', 'not in', list(self.potential_lot_ids.mapped('stock_production_lot_id.id'))),
        ])]

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

        potential_lot_ids = []

        for pl in res.get_potential_lot_ids():
            if pl.stock_quant_balance > 0:
                pl.lot_available_quantity = pl.stock_quant_balance
                potential_lot_ids.append(pl)

        regs = [
            (0, 0, potential_lot) for potential_lot in potential_lot_ids
        ]

        res.update({
            'potential_lot_ids': regs})

        stock_picking = self.env['stock.picking'].search([
            ('name', '=', res.origin)
        ])

        if stock_picking:
            stock_picking.update({
                'has_mrp_production': True
            })

        return res

    def button_plan(self):

        for stock_move in self.move_raw_ids:
            stock_move.product_uom_qty = stock_move.reserved_availability
            if stock_move.product_uom_qty == 0:
                stock_move.update({
                    'raw_material_production_id': None
                })
        self.move_raw_ids = self.move_raw_ids.filtered(
            lambda a: a.raw_material_production_id.id == self.id
        )

        return super(MrpProduction, self).button_plan()
