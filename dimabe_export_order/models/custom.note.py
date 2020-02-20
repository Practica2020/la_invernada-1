from odoo import models, fields, api

class CustomNote(models.Model):
    _name = "custom.note"

    body = fields.Text('Cuerpo')

    destiny = fields.Selection([
            ('andes', 'Los Andes'),
            ('sanantonio', 'San Antonio'),
        ], string='Destino', default='andes')

    footer = fields.Char('Pie')

    