from odoo import models, fields


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    file = fields.Binary("Attachment")
    file_name = fields.Char("File Name")