from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_date = fields.Datetime('Fecha de entrega')

    shipping_number = fields.Integer('Número Embarque')

    shipping_id = fields.Many2one(
        'custom.shipment',
        'Embarque'
    )

    required_loading_date = fields.Date(
        'custom.shipment.required_loading_date')

    contract_correlative = fields.Integer('corr')

    contract_correlative_view = fields.Char(
        'N° Orden',
        compute='_get_correlative_text'
    )

    consignee_id = fields.Many2one(
        'res.partner',
        'Consignatario',
        domain=[('customer', '=', True)]
    )

    notify_ids = fields.Many2many(
        'res.partner',
        domain=[('customer', '=', True)]
    )

    agent_id = fields.Many2one(
        'res.partner',
        'Agente',
        domain=[('is_agent', '=', True), ('commission', '>', 0)]
    )

    total_commission = fields.Float(
        'Valor Comisión',
        compute='_compute_total_commission'
    )

    charging_mode = fields.Selection(
        [
            ('piso', 'A Piso'),
            ('slip_sheet', 'Slip Sheet'),
            ('palet', 'Paletizado')
        ],
        'Modo de Carga'
    )

    booking_number = fields.Char('N° Booking')

    bl_number = fields.Char('N° BL')

    client_label = fields.Boolean('Etiqueta Cliente', default=False)

    client_label_file = fields.Binary(string='Archivo Etiqueta Cliente')

    container_number = fields.Char('N° Contenedor')

    freight_value = fields.Float('Valor Flete')

    safe_value = fields.Float('Valor Seguro')

    total_value = fields.Float(
        'Valor Total',
        compute='_compute_total_value',
        store=True
    )

    value_per_kilogram = fields.Float(
        'Valor por kilo',
        compute='_compute_value_per_kilogram',
        store=True
    )

    remarks = fields.Text('Comentarios')

    container_type = fields.Many2one(
        'custom.container.type',
        'Tipo de contenedor'
    )

    @api.model
    @api.depends('freight_value', 'safe_value')
    def _compute_total_value(self):
        print('')
        # cambiar amount_total
        # data = self.amount_total - self.freight_value - self.safe_value
        # self.total_value = data

    @api.model
    @api.depends('total_value')
    def _compute_value_per_kilogram(self):
        print('')
        # qty_total = 0
        # for line in self.order_line:
        # qty_total = qty_total + line.product_uom_qty
        # if qty_total > 0:
        # self.value_per_kilogram = self.total_value / qty_total

    @api.model
    @api.depends('agent_id')
    def _compute_total_commission(self):
        print('')
        # cambiar amount_total
        # self.total_commission = (self.agent_id.commission / 100) * self.amount_total

    @api.model
    # @api.depends('contract_id')
    def _get_correlative_text(self):
        print('')
        # if self.contract_id:
        # if self.contract_correlative == 0:
        # existing = self.contract_id.sale_order_ids.search([('name', '=', self.name)])
        # if existing:
        # self.contract_correlative = existing.contract_correlative
        # if self.contract_correlative == 0:
        # self.contract_correlative = len(self.contract_id.sale_order_ids)
        # else:
        # self.contract_correlative = 0
        # if self.contract_id.name and self.contract_correlative and self.contract_id.container_number:
        # self.contract_correlative_view = '{}-{}/{}'.format(
        # self.contract_id.name,
        # self.contract_correlative,
        # self.contract_id.container_number
        # )
        # else:
        # self.contract_correlative_view = ''
