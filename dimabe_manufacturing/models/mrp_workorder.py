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
        compute='_compute_potential_lot_planned_ids',
        inverse='_inverse_potential_lot_planned_ids'
    )

    @api.multi
    def _compute_potential_lot_planned_ids(self):
        for item in self:
            item.potential_serial_planned_ids = item.production_id.potential_lot_ids.filtered(
                lambda a: a.qty_to_reserve > 0
            ).mapped('stock_production_lot_id.stock_production_lot_serial_ids').filtered(
                lambda b: b.reserved_to_production_id == item.production_id
            )

    def _inverse_potential_lot_planned_ids(self):
        raise models.ValidationError(self.potential_serial_planned_ids.mapped('consumed'))

        for lot_serial in self.potential_serial_planned_ids:
            serial = self.production_id.potential_lot_ids.mapped(
                'stock_production_lot_id.stock_production_lot_serial_ids'
            ).filtered(
                lambda b: b.id == lot_serial.id
            )
            serial.update({
                'consumed': lot_serial.consumed
            })

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
        raise models.ValidationError(self.lot_id.name)
        self.validate_lot_code(self.lot_id.name)

        raise models.ValidationError('{} {}'.format(
            self.potential_serial_planned_ids.mapped('consumed'),
            self.qty_done
        ))

        super(MrpWorkorder, self).action_next()

        self.qty_done = 0

    def on_barcode_scanned(self, barcode):

        qty_done = self.qty_done

        custom_serial = self.validate_serial_code(barcode)
        if custom_serial:
            barcode = custom_serial.stock_production_lot_id.name

        super(MrpWorkorder, self).on_barcode_scanned(barcode)
        self.qty_done = qty_done + custom_serial.display_weight

        custom_serial.update({
            'consumed': True
        })

    @api.model
    def lot_is_byproduct(self):
        return self.finished_product_check_ids.filtered(
            lambda a: a.lot_id == self.lot_id and a.component_is_byproduct
        )

    def validate_lot_code(self, lot_code):
        if not self.lot_is_byproduct():
            if lot_code not in self.potential_serial_planned_ids.mapped('stock_production_lot_id.name'):
                lot_search = self.env['stock.production.lot'].search([
                    ('name', '=', lot_code)
                ])

                if not lot_search:
                    raise models.ValidationError('no se encontró registro asociado al código ingresado')

                if not lot_search.product_id.categ_id.reserve_ignore:
                    raise models.ValidationError(
                        'el código escaneado no se encuentra dentro de la planificación de esta producción'
                    )

    def validate_serial_code(self, barcode):

        custom_serial = self.potential_serial_planned_ids.filtered(
            lambda a: a.serial_number == barcode
        )
        if custom_serial:
            if custom_serial.consumed:
                raise models.ValidationError('este código ya ha sido consumido')
            return custom_serial
        self.validate_lot_code(barcode)

        return custom_serial

    def open_out_form_view(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.workorder',
            'views': [[self.env.ref('dimabe_manufacturing.mrp_workorder_out_form_view').id, 'form']],
            'res_id': self.id,
            'target': 'fullscreen'
        }
