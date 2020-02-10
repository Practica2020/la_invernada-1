from odoo import models, fields


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    data = fields.Char("Name")