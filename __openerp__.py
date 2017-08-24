# -*- coding: utf-8 -*-
{
    'name': "ean128Package",

    'summary': """
        Enable ean128 on packages""",

    'description': """
        Enable ean128 on packages and updating lots with relevant information. It is possible to configure ean128 structure and how to update information.
    """,

    'author': "jucapoco",
    'website': "http://www.jucapoco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse Tools',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'procurement'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'js': [
        'static/src/js/widgetsean.js',
    ],
    'qweb': [
        'static/src/xml/ean128-t.xml',
    ],
}