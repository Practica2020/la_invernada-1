from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_mrp_production = fields.Boolean(
        'tiene orden de producción',
        compute='_compute_has_mrp_production'
    )

    @api.multi
    def _compute_has_mrp_production(self):
        for item in self:
            item.has_mrp_production = len(item.env['mrp.production'].search([
                ('origin', '=', item.name)
            ])) == 1

    @api.multi
    def return_action(self):
        procurement_group = self.env['procurement.group'].search([
            ('name', '=', self.origin)
        ])

        if procurement_group:
            procurement_group = procurement_group[0]

        context = {
            'default_product_id': self.product.id,
            'default_product_uom_qty': self.quantity_done,
            'default_origin': self.name,
            'default_procurement_group_id': procurement_group.id,
            'default_requested_qty': self.quantity_done
        }

        return {
            "type": "ir.actions.act_window",
            "res_model": "mrp.production",
            "view_type": "form",
            "view_mode": "form",
            "views": [(False, "form")],
            "view_id ref='mrp.mrp_production_form_view'": '',
            "target": "current",
            "context": context
        }
