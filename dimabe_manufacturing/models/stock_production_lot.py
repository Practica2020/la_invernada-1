from odoo import fields, models, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    is_prd_lot = fields.Boolean('Es Lote de salida de Proceso')

    is_standard_weight = fields.Boolean('Series Peso Estandar')

    standard_weight = fields.Float('Peso Estandar')

    qty_standard_serial = fields.Integer('Cantidad de Series')

    stock_production_lot_serial_ids = fields.One2many(
        'stock.production.lot.serial',
        'stock_production_lot_id',
        string="Detalle"
    )

    total_serial = fields.Float(
        'Total',
        compute='_compute_total_serial'
    )

    qty_to_reserve = fields.Float('Cantidad a Reservar')

    @api.multi
    def _compute_total_serial(self):
        for item in self:
            item.total_serial = sum(item.stock_production_lot_serial_ids.mapped('display_weight'))

    @api.multi
    def write(self, values):
        for item in self:
            res = super(StockProductionLot, self).write(values)
            counter = 0
            if item.is_standard_weight:
                for counter in item.qty_standard_serial:
                    tmp = '00{}'.format(counter)
                    serial = item.stock_production_lot_serial_ids.filtered(
                        lambda a: a.serial_number == item.name + tmp[-3:]
                    )
                    if serial:
                        serial.update({
                            'display_weight': item.standard_weight
                        })
                    else:
                        item.env['stock.production.lot.serial'].create({
                            'stock_production_lot_serial_id': item.id,
                            'dislay_weight': item.standard_weight,
                            'serial_number': item.name + tmp[-3:],
                            'belong_to_prd_lot': True
                        })
            else:

                for serial in item.stock_production_lot_serial_ids:
                    counter += 1
                    tmp = '00{}'.format(counter)
                    serial.serial_number = item.name + tmp[-3:]
            return res
