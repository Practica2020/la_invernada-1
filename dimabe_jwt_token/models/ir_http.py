from odoo import exceptions, http, models
from odoo.http import request
import jwt


class ItHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_token(cls):
        # raise exceptions.AccessDenied()
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
                    request.uid = int(payload['sub'])
                    # u = request.env['res.users'].sudo().search(
                    #     [('id', '=', int(payload['sub']))]
                    # )
            except jwt.ExpiredSignatureError:
                raise exceptions.AccessDenied()
        else:
            raise exceptions.AccessDenied()
        exceptions._logger.error('AAAAA {}'.format(request.uid))
        print('')
