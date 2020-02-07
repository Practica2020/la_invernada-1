from odoo import fields, models, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def explode(self, product, quantity, picking_type=False):
        a, b = super(MrpBom, self).explode(product, quantity, picking_type=picking_type)

        raise models.ValidationError('{} ---- {}'.format(a, b))

        return res
