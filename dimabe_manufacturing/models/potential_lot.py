from odoo import fields, models, api


class PotentialLot(models.Model):
    _name = 'potential.lot'
    _description = 'posibles lotes para planificación de producción'

    name = fields.Char('lote', related='stock_production_lot_id.name')

    lot_product_id = fields.Many2one(
        'product.product',
        related='stock_production_lot_id.product_id'
    )

    lot_balance = fields.Float(
        related='stock_production_lot_id.balance'
    )

    stock_production_lot_id = fields.Many2one('stock.production.lot', 'lote potencial')

    potential_serial_ids = fields.One2many(
        'stock.production.lot.serial',
        related='stock_production_lot_id.stock_production_lot_serial_ids',
        domain=[('consumed', '=', False)]
    )

    mrp_production_id = fields.Many2one('mrp.production', 'Producción')

    mrp_production_state = fields.Selection(
        string='estado',
        related='mrp_production_id.state'
    )

    qty_to_reserve = fields.Float('Cantidad a Reservar')

    is_reserved = fields.Boolean('Reservado')

    @api.model
    def get_stock_quant(self):
        return self.stock_production_lot_id.quant_ids.filtered(
            lambda a: a.location_id.name == 'Stock'
        )

    @api.model
    def get_production_quant(self):
        return self.stock_production_lot_id.quant_ids.filtered(
            lambda a: a.location_id.name == 'Production'
        )

    @api.multi
    def reserve_stock(self):
        for item in self:
            if not item.qty_to_reserve > 0:
                raise models.ValidationError('debe agregar la cantidad a reservar')

            stock_move = item.mrp_production_id.move_raw_ids.filtered(lambda a: a.product_id == item.lot_product_id)

            stock_quant = item.get_stock_quant()

            virtual_location_production_id = item.env['stock.location'].search([
                ('usage', '=', 'production'),
                ('location_id.name', 'like', 'Virtual Locations')
            ])

            stock_quant.sudo().update({
                'reserved_quantity': stock_quant.reserved_quantity + item.qty_to_reserve
            })

            stock_move.update({
                'active_move_line_ids': [
                    (0, 0, {
                        'product_id': item.lot_product_id.id,
                        'lot_id': item.stock_production_lot_id.id,
                        'product_uom_qty': item.qty_to_reserve,
                        'product_uom_id': stock_move.product_uom.id,
                        'location_id': stock_quant.location_id.id,
                        'location_dest_id': virtual_location_production_id.id
                    })
                ]
            })

            item.is_reserved = True

    @api.multi
    def unreserved_stock(self):
        for item in self:
            stock_move = item.mrp_production_id.move_raw_ids.filtered(lambda a: a.product_id == item.lot_product_id)

            move_line = stock_move.active_move_line_ids.filtered(
                lambda a: a.lot_id.id == item.stock_production_lot_id.id
            )

            stock_quant = item.get_stock_quant()
            stock_quant.sudo().update({
                'reserved_quantity': stock_quant.reserved_quantity - item.qty_to_reserve
            })

            for ml in move_line:
                if ml.qty_done > 0:
                    raise models.ValidationError('este producto ya ha sido consumido')
                ml.write({'move_id': None, 'product_uom_qty': 0})

            item.is_reserved = False
