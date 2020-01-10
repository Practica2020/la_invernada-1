from odoo import http, exceptions
from odoo.http import request


class QualityAnalysis(http.Controller):

    @http.route('/quality_analysis', type='json', auth='token', cors='*')
    def quality_analysis_list(self):
        res = request.env['quality.analysis'].sudo().search([])
        exceptions._logger.error('controller')

        return res.read([
            'pre_caliber',
            'caliber_ids'
        ])

    @http.route('quality_analysis', type='json', auth='token', cors='*', methods=['POST'])
    def quality_analysis_post(self):
        return {
            'ok': 'ok'
        }
