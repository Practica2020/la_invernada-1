from odoo import fields, models, api


class QualityAnalysis(models.Model):
    _name = 'quality.analysis'
    _description = """
        clase que almacena los datos de calidad del sistema dimabe
    """

    stock_production_lot_ids = fields.One2many(
        'stock.production.lot',
        'quality_analysis_id',
        string='Lote'
    )

    lot_name = fields.Char(
        compute='_compute_lot_name'
    )

    name = fields.Char('Informe')

    pre_caliber = fields.Float('Precalibre')

    caliber_ids = fields.One2many(
        'caliber.analysis',
        'quality_analysis_id',
        'Análisis Calibre'
    )

    caliber_1 = fields.Float(
        '26-28',
        compute='_compute_caliber_1'
    )
    caliber_2 = fields.Float(
        '28-30',
        compute='_compute_caliber_2'
    )
    caliber_3 = fields.Float(
        '30-32',
        compute='_compute_caliber_3'
    )
    caliber_4 = fields.Float(
        '32-34',
        compute='_compute_caliber_4'
    )
    caliber_5 = fields.Float(
        '34-36',
        compute='_compute_caliber_5'
    )
    caliber_6 = fields.Float(
        '36+',
        compute='_compute_caliber_6'
    )

    @api.model
    def get_caliber(self, name):
        return self.caliber_ids.filtered(lambda a: a.name == name)

    @api.multi
    def _compute_caliber_1(self):
        for item in self:
            item.caliber_1 = item.get_caliber('26 (mm) - 28 (mm)').percent

    @api.multi
    def _compute_caliber_2(self):
        for item in self:
            item.caliber_2 = item.get_caliber('28 (mm) - 30 (mm)').percent

    @api.multi
    def _compute_caliber_3(self):
        for item in self:
            item.caliber_3 = item.get_caliber('30 (mm) - 32 (mm)').percent

    @api.multi
    def _compute_caliber_4(self):
        for item in self:
            item.caliber_4 = item.get_caliber('32 (mm) - 34 (mm)').percent

    @api.multi
    def _compute_caliber_5(self):
        for item in self:
            item.caliber_5 = item.get_caliber('34 (mm) - 36 (mm)').percent

    @api.multi
    def _compute_caliber_6(self):
        for item in self:
            item.caliber_6 = item.get_caliber('> 36 (mm)').percent

    external_damage_analysis_ids = fields.One2many(
        'external.damage.analysis',
        'quality_analysis_id',
        'Análisis Daños Externos'
    )

    external_damage_analysis_1 = fields.Float(
        'MANCHA GRAVE',
        compute='_compute_external_damage_analysis_1'
    )

    external_damage_analysis_2 = fields.Float(
        'CASCO ABIERTO',
        compute='_compute_external_damage_analysis_2'
    )

    external_damage_analysis_3 = fields.Float(
        'CÁSCARA IMPERFECTA',
        compute='_compute_external_damage_analysis_3'
    )

    external_damage_analysis_4 = fields.Float(
        'NUEZ PARTIDA',
        compute='_compute_external_damage_analysis_4'
    )

    external_damage_analysis_5 = fields.Float(
        'NUEZ TRIZADA',
        compute='_compute_external_damage_analysis_5'
    )

    @api.model
    def get_external_damage(self, name):
        return self.external_damage_analysis_ids.filtered(lambda a: a.name == name)

    @api.multi
    def _compute_external_damage_analysis_1(self):
        for item in self:
            item.external_damage_analysis_1 = item.get_external_damage('MANCHA GRAVE').percent

    @api.multi
    def _compute_external_damage_analysis_2(self):
        for item in self:
            item.external_damage_analysis_2 = item.get_external_damage('CASCO ABIERTO').percent

    @api.multi
    def _compute_external_damage_analysis_3(self):
        for item in self:
            item.external_damage_analysis_3 = item.get_external_damage('CÁSCARA IMPERFECTA').percent

    @api.multi
    def _compute_external_damage_analysis_4(self):
        for item in self:
            item.external_damage_analysis_4 = item.get_external_damage('NUEZ PARTIDA').percent

    @api.multi
    def _compute_external_damage_analysis_5(self):
        for item in self:
            item.external_damage_analysis_5 = item.get_external_damage('NUEZ TRIZADA').percent

    internal_damage_analysis_ids = fields.One2many(
        'internal.damage.analysis',
        'quality_analysis_id',
        'Análisis Daños Internos'
    )

    humidity_analysis_id = fields.Many2one('humidity.analysis', 'Análisis de Humedad')

    humidity_percent = fields.Float(
        related='humidity_analysis_id.percent'
    )

    humidity_tolerance = fields.Float(
        related='humidity_analysis_id.tolerance'
    )

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

    category = fields.Char('Categoría')

    @api.model
    def create(self, values_list):
        res = super(QualityAnalysis, self).create(values_list)
        res.name = 'Informe QA {}'.format(fields.datetime.utcnow())
        return res

    @api.multi
    @api.depends('stock_production_lot_ids')
    def _compute_lot_name(self):
        for item in self:
            if item.stock_production_lot_ids and len(item.stock_production_lot_ids) > 0:
                item.lot_name = item.stock_production_lot_ids[0].name

