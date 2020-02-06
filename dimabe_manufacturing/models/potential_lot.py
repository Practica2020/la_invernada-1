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

    @api.multi
    def reserve_stock(self):
        if not self.qty_to_reserve > 0:
            raise models.ValidationError('debe agregar la cantidad a reservar')

        models._logger.error('{} {}'.format(self.mrp_production_id, self.qty_to_reserve))
