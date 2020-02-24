from odoo import models, fields, api

class Transport(models.Model):

    _name = 'custom.transport'
   
    name = fields.Char(compute='_compute_name')
    

    is_truck = fields.Boolean('Es un camión?')
    
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
        if 'patent' in values_list:
            values_list['patent'] = str.upper(values_list['patent'])
        return values_list
    
    @api.multi
    def _compute_name(self):
        for item in self:
            item.name=item.patent
       