from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    reserve_ignore = fields.Boolean('Ignorar al reservar en producción')
