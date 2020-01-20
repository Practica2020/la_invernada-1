from odoo import fields, models,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contract_number = fields.Char('Contrato')

    @api.model()
    def __filter_clients(self):
        if self.parent_company_type == 'person':
            models._logger(self.parent_company_type)