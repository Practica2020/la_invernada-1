from odoo import fields, models, api


class PotentialLot(models.Model):
    _name = 'potential.lot'
    _description = 'posibles lotes para planificación de producción'

    name = fields.Char('lote', related='stock_production_lot_id.name')

    lot_product = fields.Many2one(
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
        if 'params' in self.env.context:
            params = self.env.context['params']
            if 'id' in params and 'model' in params and params['model'] == 'mrp.production':
                mrp_production = self.env['mrp.production'].search([('id', '=', params['id'])])
                models._logger.error('{} {}'.format(mrp_production, self.qty_to_reserve))
