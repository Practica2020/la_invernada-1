from odoo import fields, models, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    stock_production_lot_serial_ids = fields.One2many(
        'stock.production.lot.serial',
        'stock_production_lot_id',
        string="Detalle"
    )

    total_serial = fields.Float(
        'Total',
        compute='_compute_total_serial'
    )

    available_quantity = fields.Float(
        'Saldo Disponible'
    )

    qty_to_reserve = fields.Float('Cantidad a Reservar')

    stock_quant_balance = fields.Float(
        compute='_compute_stock_quant_balance'
    )

    @api.multi
    def _compute_stock_quant_balance(self):
        for item in self:
            item.stock_quant_balance = item.quant_ids.filtered(lambda a: a.location_id.name == 'Stock').balance

    @api.onchange('stock_quant_balance')
    def _compute_available_quantity(self):
        for item in self:
            raise models.ValidationError(item.stock_quant_balance)
            item.available_quantity = item.stock_quant_balance

    @api.multi
    def _compute_total_serial(self):
        for item in self:
            item.total_serial = sum(item.stock_production_lot_serial_ids.mapped('display_weight'))

    @api.multi
    def write(self, values):
        for item in self:
            res = super(StockProductionLot, self).write(values)
            counter = 0
            for serial in item.stock_production_lot_serial_ids:
                counter += 1
                tmp = '00{}'.format(counter)
                serial.serial_number = item.name + tmp[-3:]
            return res
