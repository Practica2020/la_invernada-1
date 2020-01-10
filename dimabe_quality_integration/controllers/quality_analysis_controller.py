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
    def quality_analysis_post(self, data):
        exceptions._logger.error(data)
        if 'lot' not in data:
            raise exceptions.ValidationError('debe indicar lote')
        lot = request.env['stock.production.lot'].search([('name', '=', data['lot'])])
        if not lot:
            raise exceptions.ValidationError('lote no encontrado')
        quality_analysis = request.env['quality.analysis'].create(data)
        if quality_analysis:
            lot.update({
                'quality_analysis_id': quality_analysis.id
            })

        return {
            'ok': 'ok',
            'res': data,
            'needed': {
                'data': {
                    'lot': 'char',
                    'pre_caliber': 'float',
                    'caliber_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'external_damage_analysis_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'internal_damage_analysis_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'humidity_analysis_id': {
                        {'ref', 'name', 'percent', 'tolerance'}
                    },
                    'performance_analysis_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'color_analysis_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'form_analysis_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'impurity_analysis_ids': [
                        {'ref', 'name', 'percent'}
                    ],
                    'analysis_observations': 'text',
                    'analysis_images': 'binary',
                    'category': 'char'
                }
            }
        }
