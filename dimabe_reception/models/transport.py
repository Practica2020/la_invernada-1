from odoo import models, fields, api


class Transport(models.Model):

    _name = 'custom.transport'


    transport_patent = fields.Char('Patente')

    transport_is_truck = fields.Char('Es camión?')
    

    @api.model
    def create(self, values_list):
        values_list = self._prepare_data(values_list)
        return super(Transport, self).create(values_list)

    @api.multi
    def write(self, vals):
        vals = self._prepare_data(vals)
        return super(Transport, self).write(vals)

    def _prepare_data(self, values_list):
        if 'transport_is_truck' in values_list:
            values_list['transport_is_truck'] = str.upper(values_list['transport_is_truck'])
        if 'transport_patent' in values_list:
            values_list['transport_patent'] = str.upper(values_list['transport_patent'])
        return values_list