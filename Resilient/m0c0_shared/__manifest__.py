# -*- coding: utf-8 -*-

{
    "name": "M0C0 - Base Compartida",
    "version": "0.1.4",
    "author": "MOROPO S.U.R.L.",
    'website': 'https://www.moropo.cu',
    "contact": 'contacto@moropo.cu',
    'category': 'Localization',
    "description": "",
    "depends": ["base", "contacts", "mail"],
    "data": [
        'data/res_state_municipality_data.xml',

        'views/res_partner_views.xml',
        'views/res_municipality_views.xml'

        'report/report_paperformat_data.xml',
        
        'security/ir.model.access.csv',
    ],
}