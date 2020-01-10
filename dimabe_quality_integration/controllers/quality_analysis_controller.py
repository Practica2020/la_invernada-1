from odoo import http, exceptions
from odoo.http import request


class QualityAnalysis(http.Controller):

    @http.route('/quality_analysis', type='json', auth='token', cors='*', methods=['GET'])
    def quality_analysis_list(self):
        res = request.env['quality.analysis'].sudo().search([])
        return res.read([
            'pre_caliber',
            'caliber_ids'
        ])

    @http.route('/quality_analysis', type='json', auth='token', cors='*', methods=['POST'])
    def quality_analysis_post(self, quality_analysis):
        return {
            'ok': 'ok',
            'res': quality_analysis
        }
