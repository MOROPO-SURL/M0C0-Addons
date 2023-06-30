# -*- coding: utf-8 -*-
{
    'name': 'M0C0 - Perfilado de Cierres Fiscales',
    'summary': 'Personalizaciones de cierres fiscales en la Contabilidad de M0C0 ',
    'description': 'Perfilado de formularios de cierre fiscal en la contabilidad para propiciar la realización de respaldos previos a cierres para la localización cubana de Odoo M0C0.',
    'author': 'MOROPO S.U.R.L.',
    'website': 'https://www.moropo.cu',
    'category': 'Localization',
    'version': '0.1.0',
    'depends': ['m0c0_account', 'account_fiscal_year', 'auto_backup'],
    'data': [
        'views/fiscal_year_change_lock_date_backup_remainder.xml'
    ],
    'license': 'LGPL-3',
}