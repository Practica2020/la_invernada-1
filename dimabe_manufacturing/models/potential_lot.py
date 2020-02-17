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

            item.qty_to_reserve = sum(serial_to_reserve.mapped('display_weight'))

            serial_to_reserve.reserve_serial()

            item.is_reserved = True

    @api.multi
    def unreserved_stock(self):
        for item in self:
            serial_to_reserve = item.potential_serial_ids.filtered(
                lambda a: a.reserved_to_production_id == item.mrp_production_id
            )

            serial_to_reserve.unreserved_serial()

            item.is_reserved = False
