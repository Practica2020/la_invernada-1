from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    exchange_rate = fields.Float(
        'Taza de Cambio'
    )

    @api.model
    @api.onchange('date')
    def _default_exchange_rate(self):
        date = self.date
        if date:
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')])
            rates = currency_id.rate_ids.search([('name', '=', date)])
            if len(rates) == 0:
                currency_id.get_rate_by_date(date)

            rates = self.env['res.currency.rate'].search([('name', '<=', date)])

            if len(rates) > 0:
                rate = rates[0]
                self.exchange_rate = 1 / rate.rate
        else:
            self.exchange_rate = 0