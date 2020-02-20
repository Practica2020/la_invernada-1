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
        destiny = dict(self._fields['destiny'].selection).get(self.destiny)
        full_note = self.body
        models._logger.error("Original:{}".format(full_note))
        full_note.replace("{destino}", destiny)
        models._logger.error("Modificado:{}".format(full_note))
        return self.body
