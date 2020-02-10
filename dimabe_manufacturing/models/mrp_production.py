from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stock_lots = fields.Many2one("stock.production.lot")

    client_search_id = fields.Many2one(
        'res.partner',
        'Buscar Cliente',
        nullable=True
    )

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
        potential_lot_ids = []

        domain = [
            ('product_id', 'in', list(self.move_raw_ids.mapped('product_id.id'))),
            ('name', 'not in', list(self.potential_lot_ids.mapped('stock_production_lot_id.id')))
        ]

        raise models.ValidationError(self.picking_ids)

        if self.client_search_id:

            client_lot_ids = self.env['quality.analysis'].search([
                ('potential_client_id', '=', self.picking_ids.partner_id)
            ]).mapped('stock_production_lot_ids')

            domain += ('name', 'in', client_lot_ids)

        res = self.env['stock.production.lot'].search(domain)

        for pl in res:
            if pl.stock_quant_balance > 0:
                pl.lot_available_quantity = pl.stock_quant_balance
                potential_lot_ids.append(pl)

        return [{
            'stock_production_lot_id': lot.id,
            'mrp_production_id': self.id,
            'lot_available_quantity': lot.stock_quant_balance
        } for lot in potential_lot_ids]

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

        regs = [
            (0, 0, potential_lot) for potential_lot in res.get_potential_lot_ids()
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

    @api.multi
    def button_plan(self):
        for order in self:
            # if sum(order.move_raw_ids.filtered(lambda a: a.is_mp).mapped('reserved_availability')) < order.product_qty:
            #     raise models.ValidationError('la cantidad a consumir no puede ser menor a la cantidad a producir')

            for stock_move in order.move_raw_ids:
                stock_move.product_uom_qty = stock_move.reserved_availability
                stock_move.unit_factor = stock_move.product_uom_qty / order.product_qty
                if stock_move.product_uom_qty == 0:
                    stock_move.update({
                        'raw_material_production_id': None
                    })
            order.move_raw_ids = order.move_raw_ids.filtered(
                lambda a: a.raw_material_production_id.id == order.id
            )

            # real_bom_data = []
            # real_product_qty = order.bom_id.product_qty
            #
            # order.bom_id.product_qty = order.product_uom_id._compute_quantity(order.product_qty,
            #                                                                    order.bom_id.product_uom_id)
            #
            # for bom_line in order.bom_id.bom_line_ids:
            #     raw_line = order.move_raw_ids.filtered(lambda a: a.product_id == bom_line.product_id)
            #     if raw_line:
            #         real_bom_data.append({
            #             'product_id': bom_line.product_id,
            #             'product_qty': bom_line.product_qty
            #         })
            #         bom_line.product_qty = raw_line.product_uom_qty

            res = super(MrpProduction, order).button_plan()

            # for rd in real_bom_data:
            #     bl = order.bom_id.bom_line_ids.filtered(lambda a: a.product_id == rd['product_id'])
            #     if bl:
            #         bl.product_qty = rd['product_qty']
            #
            # order.bom_id.product_qty = real_product_qty

            return res
