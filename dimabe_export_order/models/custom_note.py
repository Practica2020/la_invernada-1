from odoo import models, fields, api


class CustomNote(models.Model):
    _name = "custom.note"

    name = fields.Char(string="Nombre")

    body = fields.Text(string="Cuerpo nota")

    destiny = fields.Selection(
        selection=[('andes', 'Los Andes'), ('sanantonio', 'San Antonio'), ('valparaiso', 'Valparaiso')],
        string="Destino"
    )

    footer = fields.Text(string="Pie nota")

    @api.model
    def get_full_note(self):
        destiny = dict(self._fields['destiny'].selection).get(self.destiny)
        full_note = self.body
        full_note = full_note.replace('{destino}', destiny)
        return full_note