# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountLedgerReport(models.TransientModel):
    _name = 'account.ledger.report'
    _inherit = 'account.common.report'

    account_ids = fields.Many2many('account.account', 'account_report_rel', string='Accounts')

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_to', 'target_move', 'account_ids'])[0]
        return self.env.ref('m0c0_account.report_ledger_account').report_action(self, data)