from odoo import models, fields, api

class Transport(models.Model):
    _name = 'custom_transport'

    truck_patent = fields.Char('Patente Camión')
    cart_patent = fields.Char('Patente Carro')

    @api.model
    def create(self, values_list):
        values_list = self._prepare_data(values_list)
        return super(Transport, self).create(values_list)

    @api.multi
    def write(self, vals):
        vals = self._prepare_data(vals)
        return super(Transport, self).write(vals)

    def _prepare_data(self, values_list):
        if 'truck_patent' in values_list:
            values_list['truck_patent'] = str.upper(values_list['truck_patent'])
        if 'cart_patent' in values_list:
            values_list['cart_patent'] = str.upper(values_list['cart_patent'])
        return values_list

