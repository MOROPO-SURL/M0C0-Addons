# -*- coding: utf-8 -*-
{
    'name': 'M0C0 - Contabilidad, Reportes',
    'summary': 'Complementado Reportes para M0C0',
    'description': 'Incluyendo reportes requeridos según las normas cubanas para la localización cubana de Odoo M0C0.',
    'author': 'MOROPO S.U.R.L.',
    'website': 'https://www.moropo.cu',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '15.0.0.26',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account_financial_report'],
    # always loaded
    'data': [
        #'views/bank_reconcile_dashboard_view.xml',
        #'views/bank_reconcile_report_template.xml',
        'wizard/bank_reconcile_report_wizard_views.xml'
    ],
    'license': 'LGPL-3',
}