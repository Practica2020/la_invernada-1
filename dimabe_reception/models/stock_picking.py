from odoo import models, api, fields
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    guide_number = fields.Integer('Número de Guía')

    weight_guide = fields.Integer('Kilos Guía')

    gross_weight = fields.Integer('Kilos Brutos')

    tare_weight = fields.Integer('Peso Tara')

    net_weight = fields.Integer(
        'Kilos Netos',
        compute='_compute_net_weight',
        store=True
    )

    canning_weight = fields.Float(
        'Peso Envases',
        compute='_compute_canning_weight',
        store=True
    )

    production_net_weight = fields.Float(
        'Kilos Netos Producción',
        compute='_compute_production_net_weight',
        store=True
    )

    reception_type_selection = fields.Selection([
        ('ins', 'Insumos'),
        ('mp', 'Materia Prima')
    ],
        default='ins',
        string='Tipo de Recepción'
    )

    is_mp_reception = fields.Boolean(
        'Recepción de MP',
        compute='_compute_is_mp_reception',
        store=True
    )

    carrier_id = fields.Many2one('custom.carrier', 'Conductor')

    truck_in_date = fields.Datetime(
        'Entrada de Camión',
        readonly=True
    )

    elapsed_time = fields.Char(
        'Horas Camión en planta',
        compute='_compute_elapsed_time'
    )

    avg_unitary_weight = fields.Float(
        'Promedio Peso unitario',
        compute='_compute_avg_unitary_weight'
    )

    quality_weight = fields.Float('Kilos Calidad')

    carrier_rut = fields.Char(
        'Rut',
        related='carrier_id.rut'
    )

    carrier_cell_phone = fields.Char(
        'Celular',
        related='carrier_id.cell_number'
    )

    carrier_truck_patent = fields.Char(
        'Patente Camión',
        related='carrier_id.truck_patent'
    )

    carrier_cart_patent = fields.Char(
        'Patente Carro',
        related='carrier_id.cart_patent'
    )

    hr_alert_notification_count = fields.Integer('Conteo de notificación de retraso de camión')

    kg_diff_alert_notification_count = fields.Integer('Conteo de notificación de diferencia de kg')

    sag_code = fields.Char(
        'CSG',
        related='partner_id.sag_code'
    )

    reception_alert = fields.Many2one('reception.alert.config')

    @api.one
    @api.depends('tare_weight', 'gross_weight', 'move_ids_without_package', 'quality_weight')
    def _compute_net_weight(self):
        self.net_weight = self.gross_weight - self.tare_weight + self.quality_weight
        if self.is_mp_reception:
            if self.canning_weight:
                self.net_weight = self.net_weight - self.canning_weight

    @api.one
    @api.depends('move_ids_without_package')
    def _compute_canning_weight(self):
        canning = self.get_canning_move()
        if len(canning) == 1 and canning.product_id.weight:
            self.canning_weight = canning.product_uom_qty * canning.product_id.weight

    @api.one
    @api.depends('tare_weight', 'gross_weight', 'move_ids_without_package', )
    def _compute_production_net_weight(self):
        self.production_net_weight = self.gross_weight - self.tare_weight
        if self.is_mp_reception:
            if self.canning_weight:
                self.production_net_weight = self.production_net_weight - self.canning_weight

    @api.one
    def _compute_elapsed_time(self):
        if self.truck_in_date:
            if self.date_done:
                self.elapsed_time = self._get_hours(self.truck_in_date, self.date_done)
            else:

                self.elapsed_time = self._get_hours(self.truck_in_date, datetime.now())
        else:
            self.elapsed_time = '00:00:00'

    @api.one
    @api.depends('reception_type_selection')
    def _compute_is_mp_reception(self):
        self.is_mp_reception = self.reception_type_selection == 'mp'

    @api.one
    @api.depends('production_net_weight', 'tare_weight', 'gross_weight', 'move_ids_without_package')
    def _compute_avg_unitary_weight(self):
        if self.production_net_weight:
            canning = self.get_canning_move()
            if len(canning) == 1:
                divisor = canning.product_uom_qty
                if divisor == 0:
                    divisor = 1
                self.avg_unitary_weight = self.production_net_weight / divisor

    @api.model
    def get_mp_move(self):
        return self.move_ids_without_package.filtered(lambda x: x.product_id.categ_id.is_mp == True)

    @api.model
    def get_canning_move(self):
        return self.move_ids_without_package.filtered(lambda x: x.product_id.categ_id.is_canning == True)

    def _get_hours(self, init_date, finish_date):
        diff = str((finish_date - init_date))
        return diff.split('.')[0]

    @api.multi
    def action_confirm(self):
        for stock_picking in self:
            if stock_picking.is_mp_reception:
                stock_picking.validate_mp_reception()
                stock_picking.truck_in_date = fields.datetime.now()
            res = super(StockPicking, self).action_confirm()
            return res

    @api.multi
    def button_validate(self):
        for stock_picking in self:
            message = ''
            if stock_picking.is_mp_reception:
                if not stock_picking.gross_weight:
                    message = 'Debe agregar kg brutos \n'
                if not stock_picking.tare_weight:
                    message = 'Debe agregar kg tara'
                if message:
                    raise models.ValidationError(message)
        return super(StockPicking, self).button_validate()

    @api.model
    def validate_mp_reception(self):
        message = ''
        if not self.guide_number:
            message = 'debe agregar número de guía \n'
        if not self.weight_guide:
            message += 'debe agregar kilos guía \n'

        raise models.ValidationError('{} {} {}'.format(
            self.get_canning_move().name,
            self.get_canning_move().product_id.name,
            self.get_canning_move().quantity_done
        ))
        if not self.get_canning_move():
            message += 'debe agregar envases'
        if not self.get_mp_move():
            message += 'debe agregar MP'
        if message:
            raise models.ValidationError(message)

    @api.multi
    def get_full_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return base_url

    @api.multi
    def notify_alerts(self):
        alert_config = self.env['reception.alert.config'].search([])
        if self.hr_alert_notification_count == 0 and self.elapsed_time > alert_config.hr_alert:
            self.ensure_one()
            self.reception_alert = alert_config
            template_id = self.env.ref('dimabe_reception.truck_not_out_mail_template')
            self.message_post_with_template(template_id.id)
            self.hr_alert_notification_count += 1

        if self.kg_diff_alert_notification_count == 0:
            if self.weight_guide > 0 and self.net_weight > 0:
                if abs(self.weight_guide - self.net_weight) > alert_config.kg_diff_alert:
                    self.ensure_one()
                    self.reception_alert = alert_config
                    template_id = self.env.ref('dimabe_reception.diff_weight_alert_mail_template')
                    self.message_post_with_template(template_id.id)
                    self.kg_diff_alert_notification_count += self.kg_diff_alert_notification_count
