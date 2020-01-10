from odoo import exceptions, http, models
from odoo.http import request
import jwt


class ItHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_token(cls):
        token = request.httprequest.headers.get('authorization', '', type=str)
        if token:
            token = token.split(' ')[1]
            try:
                payload = jwt.decode(
                    token,
                    'skjdfe48ueq893rihesdio*($U*WIO$u8',
                    algorithms=['HS256']
                )
                if 'sub' in payload:
                    u = request.env['res.users'].sudo().search(
                        [('id', '=', int(payload['sub']))]
                    )
                    request.uid = u.id
            except jwt.ExpiredSignatureError:
                raise exceptions.AccessDenied()
