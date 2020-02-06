from odoo import fields, models, api


class PotentialLot(models.Model):
    _name = 'potential.lot'
    _description = 'posibles lotes para planificación de producción'

    name = fields.Char('lote', related='stock_production_lot_id.name')

    lot_product_id = fields.Many2one(
        'product.product',
        related='stock_production_lot_id.product_id'
    )

    lot_available_quantity = fields.Float(
        'Saldo Disponible',
        related='stock_production_lot_id.available_quantity'
    )

    stock_production_lot_id = fields.Many2one('stock.production.lot', 'lote potencial')

    mrp_production_id = fields.Many2one('mrp.production', 'Producción')

    qty_to_reserve = fields.Float('Cantidad a Reservar')

    is_reserved = fields.Boolean('Reservado')

    @api.multi
    def reserve_stock(self):
        if not self.qty_to_reserve > 0:
            raise models.ValidationError('debe agregar la cantidad a reservar')

        stock_move = self.mrp_production_id.move_raw_ids.filtered(lambda a: a.product_id == self.lot_product_id)

        stock_move.update({
            'active_move_line_ids': [
                (0, 0, {
                    'product_id': self.lot_product_id.id,
                    'lot_id': self.stock_production_lot_id.id,
                    'product_uom_qty': stock_move.reserved_availability + self.qty_to_reserve,
                    'product_uom_id': stock_move.product_uom.id,
                    'location_id': self.stock_production_lot_id.quant_ids.filtered(
                        lambda a: a.location_id.name == 'Stock'
                    ).location_id.id,
                    'location_dest_id': self.stock_production_lot_id.quant_ids.filtered(
                        lambda a: a.location_id.name == 'Production'
                    ).location_id.id
                })

            ]

        })

        self.is_reserved = True

    @api.multi
    def unreserved_stock(self):
        stock_move = self.mrp_production_id.move_raw_ids.filtered(lambda a: a.product_id == self.lot_product_id)

        move_line = stock_move.active_move_line_ids.filtered(lambda a: a.lot_id.id == self.stock_production_lot_id.id)

        if move_line:
            move_line[0].unlink()

        self.is_reserved = False
