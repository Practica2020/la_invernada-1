from odoo import models, fields

class CustomContainerType(models.Model):

    _name = 'custom.container.type'

    name = fields.Char(string='Tipo de Contenedor', required=True)