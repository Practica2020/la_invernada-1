from odoo import fields,models

class MrpDispatched(models.Models):
    _name = 'mrp.dispatched'
    _inherit = 'stock.picking'

    shipping_id = fields.Many2one(
        'custom.shipment',
        'Embarque'
    )

    required_loading_date = fields.Date(
        related='shipping_id.required_loading_date')

    variety = fields.Many2many(related="product_id.attribute_value_ids")

    country = fields.Char(related='partner_id.country_id.name')

    quantity_done = fields.Float(
        related='move_ids_without_package.quantity_done')

    product = fields.Many2one(related="move_ids_without_package.product_id")