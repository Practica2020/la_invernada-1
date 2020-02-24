from odoo import fields, models


class MrpDispatched(models.Model):
    _name = 'mrp.dispatched'
    _inherit = 'stock.picking'


