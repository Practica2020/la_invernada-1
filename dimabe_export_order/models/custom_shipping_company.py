from odoo import models, fields


class CustomShippingCompany(models.Model):

    _name = 'custom.shipping.company'

    name = fields.Char(string='Naviera', required=True)