from odoo import fields, models, api
from .rut_helper import prepare_rut


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_rut = fields.Char(
        'Rut Facturación'
    )

    @api.model
    def create(self, values_list):
        prepare_rut(values_list)
        return super(ResCompany, self).create(values_list)

    @api.multi
    def write(self, values):
        prepare_rut(values)
        return super(ResCompany, self).write(values)
