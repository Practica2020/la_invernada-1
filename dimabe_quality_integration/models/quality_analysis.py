from odoo import fields, models, api


class QualityAnalysis(models.Model):
    _name = 'quality.analysis'
    _description = """
        clase que almacena los datos de calidad del sistema dimabe
    """

    name = fields.Char('Informe')

    pre_caliber = fields.Float('precalibre')

    caliber_ids = fields.One2many(
        'caliber.analysis',
        'quality_analysis_id',
        'Análisis Calibre'
    )

    external_damage_analysis_ids = fields.One2many(
        'external.damage.analysis',
        'quality_analysis_id',
        'Análisis Daños Externos'
    )

    internal_damage_analysis_ids = fields.One2many(
        'internal.damage.analysis',
        'quality_analysis_id',
        'Análisis Daños Internos'
    )

    humidity_analysis_id = fields.Many2one('humidity.analysis', 'Análisis de Humedad')

    performance_analysis_ids = fields.One2many(
        'performance.analysis',
        'quality_analysis_id',
        'Análisis Rendimiento'
    )

    color_analysis_ids = fields.One2many(
        'color.analysis',
        'quality_analysis_id',
        'Análisis Color'
    )

    form_analysis_ids = fields.One2many(
        'form.analysis',
        'quality_analysis_id',
        'Análisis Forma'
    )

    impurity_analysis_ids = fields.One2many(
        'impurity.analysis',
        'quality_analysis_id',
        'Análisis Impureza'
    )

    analysis_observations = fields.Text('Observaciones')

    analysis_images = fields.Binary('Imágenes')

    category = fields.Char('Categoría')

    @api.model
    def create(self, values_list):
        res = super(QualityAnalysis, self).create(values_list)
        res.name = 'Informe QA {}'.format(fields.datetime.utcnow())
        return res
