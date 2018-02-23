# -*- coding: utf-8 -*-
# Part of Dutchworld Solutions.


{
    'name': 'Mitserv import',
    'version': '1.0',
    'category': 'Import',
    'description': """
    Customized sales order import tool
    """,
    'author': 'Dutchworld Solutions',
    'depends': ['base', 'sale_management', 'account'],
    'data': [
        'wizard/mitserv_import.xml',
        'views/sale_report_templates.xml',
        'views/res_config_settings_views.xml',
        'views/project_form_view.xml',
        'views/report_delivery_slip.xml',
        'data/emails.xml'
    ],
}
