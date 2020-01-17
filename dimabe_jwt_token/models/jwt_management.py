from odoo import models, api, fields


class JwtManagemenet(models.Model):
    _name = 'jwt.management'

    database = fields.Char('Base de Datos de Odoo')

