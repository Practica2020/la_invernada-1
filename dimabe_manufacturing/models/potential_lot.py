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

    qty_to_reserve = fields.Float('Cantidad a Reservar')
