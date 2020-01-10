# -*- coding: utf-8 -*-
from odoo import http, exceptions
from odoo.http import request
import jwt
import datetime
from xmlrpc import client


class JWTTokenController(http.Controller):
    @http.route('/api/get_token', type='json', auth='none', cors='*')
    def login(self, user, password):
        server_url = 'https://dimabe-odoo-la-invernada-dev-801206.dev.odoo.com'
        db_name = 'dimabe-odoo-la-invernada-dev-801206'
        common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
        user_id = common.authenticate(db_name, str(user), str(password), {})
        res = {}
        if user_id:
            exp = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
            }
            token = jwt.encode(
                payload,
                'skjdfe48ueq893rihesdio*($U*WIO$u8',
                algorithm='HS256'
            )
            res = {
                'user_id': user_id,
                'access_token': token
            }
        else:
            raise exceptions.AccessDenied()
        return res

    @http.route('/api/login', type='json', auth='public', cors='*')
    def do_login(self, user, password):
        # get current db
        uid = request.session.authenticate(
            'dimabe-odoo-la-invernada-dev-801206',
            user,
            password
        )
        if not uid:
            return self.errcode(code=400, message='incorrect login')
        # login success, generate token

        return self.response(data={'user': uid, 'token': 'token'})
