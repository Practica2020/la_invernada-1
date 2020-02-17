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
        domain=[('consumed', '!=', True)]
    )

    mrp_production_id = fields.Many2one('mrp.production', 'Producción')

    mrp_production_state = fields.Selection(
        string='estado',
        related='mrp_production_id.state'
    )

    qty_to_reserve = fields.Float('Cantidad Reservada')

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
            serial_to_reserve = item.potential_serial_ids.filtered(lambda a: not a.reserved_to_production_id)

            serial_to_reserve.reserve_serial()

            item.qty_to_reserve = sum(
                item.potential_serial_ids.filtered(
                    lambda a: a.reserved_to_production_id == item.mrp_production_id
                ).mapped('display_weight')
            )

            item.is_reserved = True

    @api.model
    def reserve_serial(self, serial_number):

        if not self.mrp_production_id:
            raise models.ValidationError('No se encontró la orden de producción a la que reservar el producto')

        item = self.potential_serial_ids.filtered(
            lambda a: a.serial_number == serial_number and a.consumed is False and not a.reserved_to_production_id
        )

        item.update({
            'reserved_to_production_id': self.mrp_production_id.id
        })

        stock_move = self.mrp_production_id.move_raw_ids.filtered(
            lambda a: a.product_id == item.stock_production_lot_id.product_id
        )

        stock_quant = item.stock_production_lot_id.quant_ids.filtered(
            lambda a: a.location_id.name == 'Stock'
        )

        virtual_location_production_id = item.env['stock.location'].search([
            ('usage', '=', 'production'),
            ('location_id.name', 'like', 'Virtual Locations')
        ])

        stock_quant.sudo().update({
            'reserved_quantity': stock_quant.reserved_quantity + item.display_weight
        })

        stock_move.sudo().update({
            'active_move_line_ids': [
                (0, 0, {
                    'product_id': item.stock_production_lot_id.product_id.id,
                    'lot_id': item.stock_production_lot_id.id,
                    'product_uom_qty': item.display_weight,
                    'product_uom_id': stock_move.product_uom.id,
                    'location_id': stock_quant.location_id.id,
                    'location_dest_id': virtual_location_production_id.id
                })
            ]
        })

    #     item.is_reserved = True

    @api.multi
    def unreserved_stock(self):
        for item in self:
            serial_to_reserve = item.potential_serial_ids.filtered(
                lambda a: a.reserved_to_production_id == item.mrp_production_id
            )

            serial_to_reserve.unreserved_serial()

            item.qty_to_reserve = 0

            item.is_reserved = False
