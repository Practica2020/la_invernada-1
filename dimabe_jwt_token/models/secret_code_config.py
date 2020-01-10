from odoo import fields, models, api


class SecretCodeConfig(models.TransientModel):
    _name = 'secret.code.config'
    _inherit = 'res.config.settings'

    api_secret_code = fields.Text(
        'Código Secreto'
    )



