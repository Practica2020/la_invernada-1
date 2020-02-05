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
        'Saldo Dsiponible',
        compute='_compute_available_quantity',
        store=True
    )

    qty_to_reserve = fields.Float('Cantidad a Reservar')

    @api.multi
    @api.depends('quant_ids')
    def _compute_available_quantity(self):
        for item in self:
            quant_id = item.quant_ids.filtered(lambda a: a.location_id.name == 'Stock')
            item.available_quantity = quant_id.balance

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

    @api.multi
    def reserve_stock(self):
        if not self.qty_to_reserve > 0:
            raise models.ValidationError('debe agregar la cantidad a reservar')
        if 'params' in self.env.context:
            params = self.env.context['params']
            if 'id' in params and 'model' in params and params['model'] == 'mrp.production':
                mrp_production = self.env['mrp.production'].search([('id', '=', params['id'])])
                models._logger.error(mrp_production)

