from odoo import models, fields

class ResCompany(models.Model):
    sag_code = fields.Char('Código Sag')