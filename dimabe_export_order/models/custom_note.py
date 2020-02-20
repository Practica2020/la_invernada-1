from odoo import models, fields, api


class CustomNote(models.Model):
    _name = "custom.note"

    body = fields.Text(string="Cuerpo nota")

    destiny = fields.Selection(
        selection=[('andes', 'Los Andes'), ('sanantonio', 'San Antonio'), ('valparaiso', 'Valparaiso')],
        string="Destino"
    )

    footer = fields.Text(string="Pie nota")

    @api.model
    def get_full_note(self):
        self.body.replace('{destino}',dict(self._fields['destiny'].selection).get(self.destiny))
        return self.body
