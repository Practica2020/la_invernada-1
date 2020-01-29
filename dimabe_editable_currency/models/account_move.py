from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    exchange_rate = fields.Float(
        'Taza de Cambio'
    )


    def action_post(self):

        if self.id:
            if not self.exchange_rate or self.exchange_rate == 0:
                raise models.ValidationError('debe existir una taza de cambio')

        return super(AccountMove, self).action_post()

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

    @api.multi
    def compute_move_totals(self, company_currency, move_lines):
        total = 0
        total_currency = 0
        for line in move_lines:
            models._logger.error('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            models._logger.error(line)
            if line.currency_id != company_currency:
                currency = line.currency_id
                date = self._get_currency_rate_date() or fields.Date.context_today(self)
                line['currency_id'] = currency.id
                line['amount_currency'] = currency.round(line['price'])
                line['price'] = currency.with_context(
                    optional_usd=self.exchange_rate
                )._convert(line['price'], company_currency, self.company_id, date)
        return total, total_currency, move_lines