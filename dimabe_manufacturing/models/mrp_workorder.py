from odoo import fields, models, api


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    production_finished_move_line_ids = fields.One2many(
        string='Productos Finalizados',
        related='production_id.finished_move_line_ids'
    )

    material_product_ids = fields.One2many(
        'product.product',
        compute='_compute_material_product_ids'
    )

    byproduct_move_line_ids = fields.One2many(
        'stock.move.line',
        compute='_compute_byproduct_move_line_ids',
        string='subproductos'
    )

    potential_serial_planned_ids = fields.One2many(
        'stock.production.lot.serial',
        compute='_compute_potential_lot_planned_ids'
    )

    @api.multi
    def _compute_potential_lot_planned_ids(self):
        for item in self:
            item.potential_serial_planned_ids = item.production_id.potential_lot_ids.filtered(
                lambda a: a.qty_to_reserve > 0
            ).mapped('potential_serial_ids').filtered(
                lambda b: b.reserved_to_production_id == item.production_id
            )

    @api.multi
    def _compute_byproduct_move_line_ids(self):
        for item in self:
            item.byproduct_move_line_ids = item.active_move_line_ids.filtered(lambda a: not a.is_raw)

    @api.multi
    def _compute_material_product_ids(self):
        for item in self:
            item.material_product_ids = item.production_id.move_raw_ids.mapped('product_id')

    @api.model
    def create(self, values_list):
        res = super(MrpWorkorder, self).create(values_list)

        name = self.env['ir.sequence'].next_by_code('mrp.workorder')

        final_lot = self.env['stock.production.lot'].create({
            'name': name,
            'product_id': res.product_id.id,
            'is_prd_lot': True
        })

        res.final_lot_id = final_lot.id

        return res

    @api.multi
    def write(self, vals):

        for item in self:

            if item.active_move_line_ids and \
                    not item.active_move_line_ids.filtered(lambda a: a.is_raw):
                for move_line in item.active_move_line_ids:
                    move_line.update({
                        'is_raw': True
                    })
                # raise models.ValidationError(item.active_move_line_ids)

        res = super(MrpWorkorder, self).write(vals)

        return res

    def open_tablet_view(self):

        for check in self.finished_product_check_ids:

            if check.component_is_byproduct:
                if not check.lot_id:
                    lot_tmp = self.env['stock.production.lot'].create({
                        'name': self.env['ir.sequence'].next_by_code('mrp.workorder'),
                        'product_id': check.component_id.id,
                        'is_prd_lot': True
                    })
                    check.lot_id = lot_tmp.id
                if check.quality_state == 'none':
                    self.action_next()

            else:
                if not check.component_id.categ_id.is_canning:
                    check.qty_done = 0
                self.action_skip()

        self.action_first_skipped_step()

        return super(MrpWorkorder, self).open_tablet_view()

    def action_next(self):
        self.validate_code(self.lot_id.name)
        return super(MrpWorkorder, self).action_next()

    def on_barcode_scanned(self, barcode):

        qty_done = self.qty_done

        custom_serial = self.validate_code(barcode)
        barcode = custom_serial.stock_production_lot_id.name
        custom_serial.write({
            'consumed': True
        })
        super(MrpWorkorder, self).on_barcode_scanned(barcode)
        self.qty_done = qty_done + custom_serial.display_weight
        self.test_type = 'register_consumed_materials'

    def validate_code(self, barcode):
        custom_serial = self.env['stock.production.lot.serial'].search([
            '|',
            ('serial_number', '=', barcode),
            ('stock_production_lot_id.name', '=', barcode)
        ])

        if custom_serial:
            if custom_serial.consumed:
                raise models.ValidationError('este código ya ha sido consumido')
            if not custom_serial.stock_production_lot_id.product_id.categ_id.reserve_ignore:
                if not self.potential_serial_planned_ids.filtered(
                        lambda a: a.serial_number == barcode
                ):
                    raise models.ValidationError(
                        'el código escaneado no se encuentra dentro de la planificación de esta producción')

        return custom_serial

    def open_out_form_view(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.workorder',
            'views': [[self.env.ref('dimabe_manufacturing.mrp_workorder_out_form_view').id, 'form']],
            'res_id': self.id,
            'target': 'fullscreen'
        }
