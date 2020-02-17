from odoo import fields, models, api


class StockProductionLotSerial(models.Model):
    _inherit = 'stock.production.lot.serial'

    production_id = fields.Many2one(
        'mrp.production',
        'Productión'
    )

    belongs_to_prd_lot = fields.Boolean(
        'pertenece a lote productivo',
        related='stock_production_lot_id.is_prd_lot'
    )

    reserved_to_production_id = fields.Many2one(
        'mrp.production',
        'Para Producción',
        nullable=True
    )

    consumed = fields.Boolean('Consumido')

    @api.model
    def create(self, values_list):
        res = super(StockProductionLotSerial, self).create(values_list)
        stock_move_line = self.env['stock.move.line'].search([
            ('lot_id', '=', res.stock_production_lot_id.id),
            ('lot_id.is_prd_lot', '=', True)
        ])
        if stock_move_line.move_id.production_id:
            res.production_id = stock_move_line.move_id.production_id[0].id
        else:
            work_order = self.env['mrp.workorder'].search([
                ('final_lot_id', '=', res.stock_production_lot_id.id)
            ])
            if work_order.production_id:
                res.production_id = work_order.production_id[0].id
        return res

    @api.multi
    def print_serial_label(self):
        return self.env.ref('dimabe_manufacturing.action_stock_production_lot_serial_label_report')\
            .report_action(self)

    @api.multi
    def get_full_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return base_url

    @api.multi
    def reserve_serial(self):
        if 'params' in self.env.context and 'id'in self.env.context['params']:
            production_id = self.env.context['params']['id']
            for item in self:
                item.update({
                    'reserved_to_production_id': production_id
                })
                # item.consumed = True

    @api.multi
    def unreserved_serial(self):
        for item in self:
            item.update({
                'reserved_to_production_id': None
            })
            # item.consumed = False
