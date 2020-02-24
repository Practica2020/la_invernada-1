from odoo import models, fields


class CustomShip(models.Model):
    _name = 'custom.ship'

    name = fields.Char(string='Nave', required=True)