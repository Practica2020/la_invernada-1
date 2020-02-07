from odoo import fields, models, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def explode(self, product, quantity, picking_type=False):
        bom, lines = super(MrpBom, self).explode(product, quantity, picking_type=picking_type)

        for line in lines:
            print()

        raise models.ValidationError('{} ---- {}'.format(bom, lines))

        return bom, lines
