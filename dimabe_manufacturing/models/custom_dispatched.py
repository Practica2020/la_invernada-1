from odoo import fields, models


class CustomDispatched(models.Model):
    _name = 'custom.dispatched'

    shipping_number = fields.Integer('Numero de Embaque')

    charging_mode = fields.Selection(
        [
            ('piso', 'A Piso'),
            ('slip_sheet', 'Slip Sheet'),
            ('palet', 'Paletizado')
        ],
        'Modo de Carga'
    )

    client_label = fields.Boolean('Etiqueta de Cliente')

    required_loading_date = fields.Date('Fecha de requerida de carga')

