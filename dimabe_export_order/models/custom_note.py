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
        message = list(self.body)
        index = 0
        for letter in message:
            models._logger.error(letter)
            index += 1
        return self.body + self.destiny + self.footer
