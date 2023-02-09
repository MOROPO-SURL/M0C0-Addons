# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import time
import math

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    line_fictions_ids = fields.One2many('account.bank.statement.line.fictions', 'statement_id', string='Statement lines fictions',
                               states={'confirm': [('readonly', True)]}, copy=True)
    total_entry_encoding_fictions = fields.Monetary('Transactions Fictions Subtotal', compute='_end_balance', store=True, help="Total of transaction fictions lines.")

    @api.one
    @api.depends('line_fictions_ids','line_fictions_ids.amount','line_ids', 'balance_start', 'line_ids.amount', 'balance_end_real')
    def _end_balance(self):
        self.total_entry_encoding_fictions = sum([line.amount for line in self.line_fictions_ids])
        self.total_entry_encoding = sum([line.amount for line in self.line_ids])
        self.balance_end = self.balance_start + self.total_entry_encoding + self.total_entry_encoding_fictions
        self.difference = self.balance_end_real - self.balance_end


class AccountBankStatementLinefictions(models.Model):
    _name = "account.bank.statement.line.fictions"
    _description = "Bank Statement Line correction"
    _order = "statement_id desc, date desc, sequence, id desc"
    _rec_name = 'ref'

    date = fields.Date(required=True, default=lambda self: self._context.get('date', fields.Date.context_today(self)))
    amount = fields.Monetary(digits=0, currency_field='journal_currency_id')
    line_type = fields.Selection([('error', 'Error'), ('correction', 'Correction')], 'Type',
                            required=True, default='error')
    journal_currency_id = fields.Many2one('res.currency', related='statement_id.currency_id',
        help='Utility field to express amount currency', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    bank_account_id = fields.Many2one('res.partner.bank', string='Bank Account')
    statement_id = fields.Many2one('account.bank.statement', string='Statement', index=True, required=True, ondelete='cascade')
    partner_name = fields.Char(help="This field is used to record the third party name when importing bank statement in electronic format,"
             " when the partner doesn't exist yet in the database (or cannot be found).")
    ref = fields.Char(string='Reference', required=True)
    note = fields.Text(string='Notes')
    sequence = fields.Integer(index=True, help="Gives the sequence order when displaying a list of bank statement lines.", default=1)
    company_id = fields.Many2one('res.company', related='statement_id.company_id', string='Company', store=True, readonly=True)
    amount_currency = fields.Monetary(help="The amount expressed in an optional other currency if it is a multi-currency entry.")
    currency_id = fields.Many2one('res.currency', string='Currency', help="The optional other currency if it is a multi-currency entry.")
    state = fields.Selection(related='statement_id.state', string='Status', readonly=True)
    correction_id = fields.Many2one('account.bank.statement.line.fictions', 'Correction', readonly=True, copy=False, index=True)
    difference_ids = fields.One2many('account.bank.statement.line.fictions', 'correction_id', string='Differences',
                                    copy=False, ondelete='restrict')

    @api.one
    @api.constrains('amount')
    def _check_amount(self):
        # Allow to enter bank statement line with an amount of 0,
        # so that user can enter/import the exact bank statement they have received from their bank in Odoo
        if self.statement_id.journal_id.type != 'bank' and self.currency_id.is_zero(self.amount):
            raise ValidationError(_('A Cash transaction can\'t have a 0 amount.'))

    @api.one
    @api.constrains('amount', 'amount_currency')
    def _check_amount_currency(self):
        if self.amount_currency != 0 and self.amount == 0:
            raise ValidationError(_('If "Amount Currency" is specified, then "Amount" must be as well.'))

    @api.onchange('difference_ids')
    def _onchange_difference_ids(self):
        amount = 0
        if self.correction_id != False:
            for difference in self.difference_ids:
                amount -= difference.amount
                self.correction_id = difference
            self.amount = amount
        else:
            self.amount = 0
            self.correction_id = False