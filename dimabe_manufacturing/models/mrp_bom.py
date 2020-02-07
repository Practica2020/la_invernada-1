from odoo import fields, models, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def explode(self, product, quantity, picking_type=False):
        res = super(MrpBom, self).explode(product, quantity, picking_type=picking_type)

        raise models.ValidationError(res)

        return res
