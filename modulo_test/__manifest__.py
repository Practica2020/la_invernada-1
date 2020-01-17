# -*- coding: utf-8 -*-
{
    'name': "mi modulo bakan",

    'summary': """
       descripción corta""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dimabe ltda",
    'website': "http://www.dimabe.cl/modulos",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'dimabe_export_order'

    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/stock_picking.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}