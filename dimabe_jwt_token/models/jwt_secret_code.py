from odoo import fields, models, api


class JWTSecretCode(models.Model):
    _name = 'jwt.secret.code'

    secret = fields.Text('Código Secreto')