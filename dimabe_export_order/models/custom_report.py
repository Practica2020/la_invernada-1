from odoo import models,fields

class CustomReport(models.Model):
    _inherit = "ir.attachment" 
    _name= "custom.report"

    file_name = fields.Char("Nombre del Archivo")

    file = fields.Binary("Archivo")

    file_extension = fields.Char("Extension") 
