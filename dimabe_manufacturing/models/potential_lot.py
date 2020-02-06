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

        stock_move.reserved_availability += self.qty_to_reserve

        self.is_reserved = True

    @api.multi
    def unreserved_stock(self):

        stock_move = self.mrp_production_id.move_raw_ids.filtered(lambda a: a.product_id == self.lot_product_id)

        stock_move.reserved_availability -= self.qty_to_reserve

        self.is_reserved = False

