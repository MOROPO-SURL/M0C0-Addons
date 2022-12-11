# -*- coding: utf-8 -*-
{
    'name': 'M0C0 - Contabilidad, Reportes',
    'summary': 'Complementado Reportes para M0C0',
    'description': 'Incluyendo reportes requeridos según las normas cubanas para la localización cubana de Odoo M0C0.',
    'author': 'MOROPO S.U.R.L.',
    'website': 'https://www.moropo.cu',
    'category': 'Localization',
    'version': '15.0.0.52',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account_financial_report', 'l10n_cu_reports'],
    # always loaded
    'data': [
        #'views/bank_reconcile_dashboard_view.xml',
        'report/bank_reconcile_report_template.xml',
        'wizard/bank_reconcile_report_wizard_views.xml',
        'security/ir.model.access.csv'
    ],
    'license': 'LGPL-3',
}