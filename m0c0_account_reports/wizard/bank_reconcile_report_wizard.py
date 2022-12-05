# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class M0C0BankReconcileReportWizard(models.TransientModel):
    _name = 'm0c0.account.bank.reconcile.report'
    _inherit = "account.common.report"

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type', '=', 'bank')])
    reconcile_date = fields.Date(string="Reconcile Date", required=True, default=fields.Date.today)
    sort_selection = fields.Selection(
        [('date', 'Date'), ('move_name', 'Journal Entry Number'), ], 
        'Entries Sorted by',
        required=True, 
        default='move_name')

    @api.multi
    def check_report(self):
        self.ensure_one()
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'journal_id': self.journal_id.id,
                'reconcile_date': self.reconcile_date,
                'sort_selection': self.sort_selection,
                'target_move': self.target_move,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('m0c0_account_reports.bank_reconcile_report').report_action(self, data=data)



