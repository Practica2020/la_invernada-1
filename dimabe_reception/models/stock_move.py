from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    has_serial_generated = fields.Boolean(
        'tiene series generadas'
    )

    is_mp = fields.Boolean(
        'es mp',
        related='product_id.categ_id.is_mp'
    )

    product_id = fields.Many2one(
        'product.product',
        'Product',
        domain=lambda self: self._domain_filter(),
        index=True,
        required=True,
        states={'done': [('readonly', True)]}
    )

    products_can_be_stored = fields.Many2many(
        'product.category',
        'productos que pueden ser almacenados',
        related='picking_type_id.warehouse_id.products_can_be_stored'
    )

    def _domain_filter(self):
        domain = [
            ('type', 'in', ['product', 'consu']),
            # ('categ_id', 'in', self.picking_type_id.warehouse_id.products_can_be_stored)
        ]
        return domain
