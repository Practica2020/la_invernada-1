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
    
    @api.onchange('amount_currency', 'currency_id')
    def _onchange_amount_currency(self):
        '''Recompute the debit/credit based on amount_currency/currency_id and date.
        However, date is a related field on account.move. Then, this onchange will not be triggered
        by the form view by changing the date on the account.move.
        To fix this problem, see _onchange_date method on account.move.
        '''
        for line in self:
            amount = line.amount_currency
            if line.currency_id and line.currency_id != line.company_currency_id:
                amount = line.currency_id.with_context(optional_usd=self.exchange_rate).compute(amount, line.company_currency_id)
                line.debit = amount > 0 and amount or 0.0
                line.credit = amount < 0 and -amount or 0.0