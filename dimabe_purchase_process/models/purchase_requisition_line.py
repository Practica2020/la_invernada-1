from odoo import fields, models, api


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        required=True
    )
