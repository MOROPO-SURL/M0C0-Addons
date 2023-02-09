# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    include_m0c0_account_financial_report = fields.Boolean("Informes Contables",
                                                             help="By checking this option, the "
                                                                  "m0c0_account_financial_report module "
                                                                  "will be installed")
    include_m0c0_mis_builder = fields.Boolean("Generador de Reportes",
                                                help="By checking this option, the m0c0_account_report_builder module "
                                                     "will be installed")
    income_account_type_ids = fields.Many2many('account.account.type', 'income_type_rel',
                                               string='Income Account Types', domain="[('type','=', 'other')]",
                                               related="company_id.income_account_type_ids")
    expense_account_type_ids = fields.Many2many('account.account.type', 'expense_type_rel',
                                                string='Expense Account Types', domain="[('type','=', 'other')]",
                                                related="company_id.expense_account_type_ids")

    @api.onchange('income_account_type_ids', 'expense_account_type_ids')
    def _onchange_income_account_type_ids(self):
        return {
            'domain': {'income_account_type_ids': [('type', '=', 'other'),
                                                   ('id', 'not in', self.expense_account_type_ids.ids)],
                       'expense_account_type_ids': [('type', '=', 'other'),
                                                    ('id', 'not in', self.income_account_type_ids.ids)]
                       }
        }