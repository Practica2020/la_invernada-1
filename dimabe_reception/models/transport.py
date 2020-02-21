from odoo import models, fields, api

class Transport(models.Model):

    _name = 'custom.transport'

    is_truck = fields.Boolean('Es camión?')
    
    patent = fields.Char('Patente')

    @api.model
    def create(self, values_list):
        values_list = self._prepare_data(values_list)
        return super(Transport, self).create(values_list)

    @api.multi
    def write(self, vals):
        vals = self._prepare_data(vals)
        return super(Transport, self).write(vals)

    def _prepare_data(self, values_list):
        if 'is_truck' in values_list:
            values_list['is_truck'] = str.upper(values_list['is_truck'])
        if 'patent' in values_list:
            values_list['patent'] = str.upper(values_list['patent'])
        return values_list