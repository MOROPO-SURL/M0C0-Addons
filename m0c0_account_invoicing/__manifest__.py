# -*- coding: utf-8 -*-
{
    'name': 'M0C0 - Contabilidad, Facturas',
    'summary': 'Homologación de Facturas dentro de la cintabilidad de M0C0',
    'description': 'Homologación de facturas de ventas dentro de la cintabilidad de M0C0 a las normas cubanas para la localización cubana de Odoo M0C0.',
    'author': 'MOROPO S.U.R.L.',
    'website': 'https://www.moropo.cu',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '15.0.0.11',
    # any module necessary for this one to work correctly
    'depends': ['base','account'],
    # always loaded
    'data': [
        'views/account_invoice_ext_globals_layout.xml',
        'views/account_invoice_ext_globals_and_signblocks.xml'
    ],
    'license': 'LGPL-3',
}