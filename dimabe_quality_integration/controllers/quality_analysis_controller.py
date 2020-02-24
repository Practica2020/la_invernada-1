from odoo import http, exceptions
from odoo.http import request


def to_tuple_list(data):
    return [
        (0, 0, reg) for reg in data
    ]


def process_child(data, field):
    if field in data and len(data[field]) > 0:
        data[field] = to_tuple_list(data[field])


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
        if 'lot' not in data:
            raise exceptions.ValidationError('debe indicar lote')
        lot = request.env['stock.production.lot'].search([('name', '=', data['lot'])])
        if not lot:
            raise exceptions.ValidationError('lote no encontrado')

        for data_list in ['caliber_ids', 'external_damage_analysis_ids', 'internal_damage_analysis_ids',
                          'performance_analysis_ids', 'color_analysis_ids', 'form_analysis_ids',
                          'impurity_analysis_ids']:
            process_child(data, data_list)

        if 'humidity_analysis_id' in data:
            humidity_analysis = request.env['humidity.analysis'].create(data['humidity_analysis_id'])
            data['humidity_analysis_id'] = humidity_analysis.id

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
                        'ref', 'name', 'percent', 'tolerance'
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

