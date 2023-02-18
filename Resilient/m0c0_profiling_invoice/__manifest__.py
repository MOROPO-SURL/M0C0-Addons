# -*- coding: utf-8 -*-
{
    'name': 'M0C0 - Perfilado de Facturas',
    'summary': 'Homologación de Facturas dentro de la cintabilidad de M0C0',
    'description': 'Homologación de facturas de ventas dentro de la cintabilidad de M0C0 a las normas cubanas para la localización cubana de Odoo M0C0.',
    'author': 'MOROPO S.U.R.L.',
    'website': 'https://www.moropo.cu',
    'category': 'Localization',
    'version': '0.3.0'
    'depends': ['account'],
    'data': [
        'views/account_invoice_globals.xml',
        'views/account_invoice_signblocks.xml'
    ],
    'license': 'LGPL-3',
}