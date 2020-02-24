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
        'mrp_production_id',
        'Posibles Lotes'
    )

    @api.onchange('client_search_id')
    def onchange_client_search_id(self):
        for production in self:
            filtered_lot_ids = production.get_potential_lot_ids()

            production.update({
                'potential_lot_ids': [
                    (2, to_unlink_id.id) for to_unlink_id in production.potential_lot_ids.filtered(
                        lambda a: a.qty_to_reserve <= 0
                    )]
            })

            to_keep = [
                (4, to_keep_id.id) for to_keep_id in production.potential_lot_ids.filtered(
                    lambda a: a.qty_to_reserve > 0
                )]

            to_add = []

            for filtered_lot_id in filtered_lot_ids:
                if not production.potential_lot_ids.filtered(
                        lambda a: a.stock_production_lot_id.id == filtered_lot_id['stock_production_lot_id']
                ):
                    to_add.append(filtered_lot_id)

            to_add_processed = []

            for new_add in to_add:
                tmp_id = self.env['potential.lot'].create(new_add)
                to_add_processed.append((4, tmp_id.id))

            production.update({
                'potential_lot_ids': to_add_processed + to_keep
            })

    @api.model
    def get_potential_lot_ids(self):
        domain = [('lot_balance', '>', 0)]
        res = []
        if self.client_search_id:
            client_lot_ids = self.env['quality.analysis'].search([
                ('potential_client_id', '=', self.client_search_id.id),
                ('potential_workcenter_id.id', 'in', list(self.routing_id.operation_ids.mapped('workcenter_id.id')))
            ]).mapped('stock_production_lot_ids.name')

            domain += [('name', 'in', list(client_lot_ids) if client_lot_ids else [])]

            res = self.env['stock.production.lot'].search(domain)

        # for pl in res:
        #     if pl.balance > 0:
        #         pl.lot_balance = pl.balance
        #         potential_lot_ids.append(pl)

        return [{
            'stock_production_lot_id': lot.id,
            'mrp_production_id': self.id
        } for lot in res]

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
            total_reserved = sum(order.move_raw_ids.filtered(
                lambda a: not a.product_id.categ_id.reserve_ignore).mapped('reserved_availability')
                                 )
            if total_reserved < order.product_qty:
                raise models.ValidationError(
                    'la cantidad a consumir ({}) no puede ser menor a la cantidad a producir ({})'.format(
                        total_reserved, order.product_qty
                    )
                )

            for stock_move in order.move_raw_ids:
                if not stock_move.product_id.categ_id.reserve_ignore:
                    stock_move.product_uom_qty = stock_move.reserved_availability

                if stock_move.product_uom_qty % 1 > 0 and stock_move.product_uom.category_id.measure_type == 'unit':
                    stock_move.product_uom_qty = stock_move.product_uom_qty + 1 - stock_move.product_uom_qty % 1

                stock_move.unit_factor = stock_move.product_uom_qty / order.product_qty
                if stock_move.product_uom_qty == 0 and not stock_move.product_id.categ_id.reserve_ignore:
                    models._logger.error('{} {}'.format(stock_move.product_id.categ_id.name,
                                                        stock_move.product_id.categ_id.reserve_ignore))
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
