# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from ..api_env import db
from ..jwt_token import generate_token


class JWTTokenController(http.Controller):

    @http.route('/api/login', type='json', auth='public', cors='*')
    def do_login(self, user, password):

        uid = request.session.authenticate(
            db,
            user,
            password
        )
        if not uid:
            return self.errcode(code=400, message='incorrect login')

        token = generate_token(uid)

        return {'user': uid, 'token': token}
