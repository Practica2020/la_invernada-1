from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    client_label_file = fields.Binary(string='Etiqueta Cliente')
