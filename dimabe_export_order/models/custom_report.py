from odoo import models, fields,api


class CustomReport(models.Model):
    _name="custom.report"
    _inherit = 'ir.attachment'

    file = fields.Binary("Attachment")
    file_name = fields.Char("File Name")
