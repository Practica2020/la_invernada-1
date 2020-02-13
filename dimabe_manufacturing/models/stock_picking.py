from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_mrp_production = fields.Boolean('tiene orden de producción')

    shipping_id = fields.Many2one(
        'custom.shipment',
        'Embarque'
    )

    required_loading_date = fields.Date(
        related='shipping_id.required_loading_date')

    variety = fields.Many2many(related="product_id.attribute_value_ids")

    country_id = fields.Char(related='partner_id.country_id.name')

    product_id = fields.Many2one(related="sale_id.order_line.product_id")

    quantity_done = fields.Float(compute='_compute_quantity_done')

    @api.multi
    def _compute_quantity_done(self):
        for item in self:
            if item.product_id and len(item.product_id) == 1:
                item.quantity_done = item.product_id.product_uom_qty

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
            'default_client_search_id': self.partner_id.id,
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
