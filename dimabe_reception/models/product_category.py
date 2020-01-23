from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    warehouse_ids = fields.Many2many(
        'stock.warehouse',
        string='Bodegas en las que se puede almacenar'
    )

    is_mp = fields.Boolean(
        'Es MP',
        compute='_compute_is_mp'
    )

    is_canning = fields.Boolean(
        'Es Envase',
        compute='_compute_is_canning'
    )

    @api.one
    def _compute_is_mp(self):
        self.is_mp = 'Materia Prima' in self.name
        if not self.is_mp and self.parent_id:
            self.is_mp = self.parent_id.is_mp

    @api.one
    def _compute_is_canning(self):
        self.is_canning = self.name == 'Envases'
        if not self.is_canning and self.parent_id:
            self.is_canning = self.parent_id.is_canning
