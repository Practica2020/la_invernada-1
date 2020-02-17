from odoo import fields, models, api


class StockProductionLotSerial(models.Model):
    _inherit = 'stock.production.lot.serial'

    is_reserved = fields.Boolean('Resevado')

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
        return self.env.ref('dimabe_manufacturing.action_stock_production_lot_serial_label_report') \
            .report_action(self)

    @api.multi
    def get_full_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return base_url

    @api.onchange('is_reserved')
    def onchange_is_reserved(self):
        for item in self:
            if item.is_reserved:
                item.reserve_serial()
            else:
                item.unreserved_serial()

    @api.model
    def reserve_serial(self):
        if 'params' in self.env.context and 'id' in self.env.context['params']:
            production_id = self.env.context['params']['id']
            production = self.env['mrp.production'].search([('id', '=', production_id)])
            if not production:
                raise models.ValidationError('No se encontró la orden de producción a la que reservar el producto')
            # for item in self:
            self.update({
                'reserved_to_production_id': production.id
            })

            stock_move = production.move_raw_ids.filtered(
                lambda a: a.product_id == self.stock_production_lot_id.product_id
            )

            stock_quant = self.stock_production_lot_id.quant_ids.filtered(
                lambda a: a.location_id.name == 'Stock'
            )

            virtual_location_production_id = self.env['stock.location'].search([
                ('usage', '=', 'production'),
                ('location_id.name', 'like', 'Virtual Locations')
            ])

            stock_quant.sudo().update({
                'reserved_quantity': stock_quant.reserved_quantity + self.display_weight
            })

            stock_move.sudo().update({
                'active_move_line_ids': [
                    (0, 0, {
                        'product_id': self.stock_production_lot_id.product_id.id,
                        'lot_id': self.stock_production_lot_id.id,
                        'product_uom_qty': self.display_weight,
                        'product_uom_id': stock_move.product_uom.id,
                        'location_id': stock_quant.location_id.id,
                        'location_dest_id': virtual_location_production_id.id
                    })
                ]
            })

        #     item.is_reserved = True

    @api.model
    def unreserved_serial(self):
        # for item in self:

        stock_move = self.reserved_to_production_id.move_raw_ids.filtered(
            lambda a: a.product_id == self.stock_production_lot_id.product_id
        )

        move_line = stock_move.active_move_line_ids.filtered(
            lambda a: a.lot_id.id == self.stock_production_lot_id.id
        )

        stock_quant = self.stock_production_lot_id.quant_ids.filtered(
            lambda a: a.location_id.name == 'Stock'
        )
        stock_quant.sudo().update({
            'reserved_quantity': stock_quant.reserved_quantity - self.display_weight
        })

        self.update({
            'reserved_to_production_id': None
        })

        for ml in move_line:
            if ml.qty_done > 0:
                raise models.ValidationError('este producto ya ha sido consumido')
            ml.write({'move_id': None, 'product_uom_qty': 0})

            # item.is_reserved = False
