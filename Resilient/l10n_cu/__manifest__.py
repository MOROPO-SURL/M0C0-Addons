# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>
# Yusnel Rojas Garcia
# Julio Smith
# Segu

{
    'name': 'M0C0 - Localización de Contabilidad para Cuba',
    'version': '0.4.2',
    'author': 'Idola Odoo Team, Comunidad cubana de Odoo, MOROPO S.U.R.L.',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
        Cuban charts of accounts.
            * Defines the following chart of account templates:
                * Cuban general chart of accounts by 494/2016 modified by 407/2019
                * Cuban general chart of accounts for Actividad Empresarial
                * Cuban general chart of accounts for Unidades Presupuestadas de Tratamiento Especial 
                * Cuban general chart of accounts for Sector Cooperativo Agropecuario y no Agropecuario"
    """,
    'depends': [
        'account',
    ],
    'data': [
        'data/account_chart_data.xml',
        'data/account.account.template-tcp.csv',
        'data/account.account.template-common.csv',
        'data/account.account.template-private.csv',
        'data/account.account.template-public.csv',
        'data/account_chart_post_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_fiscal_position_tax_template_data.xml',
        'data/account_chart_template_data.xml',
    ],
    'license': 'LGPL-3',
}
