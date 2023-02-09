# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from odoo.addons import decimal_precision as dp
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError
import calendar

class ResCompany(models.Model):
    _inherit = "res.company"

    income_account_type_ids = fields.Many2many('account.account.type', 'income_type_rel', string='Income Account Types',
                                               domain="[('type','=', 'other')]")
    expense_account_type_ids = fields.Many2many('account.account.type', 'expense_type_rel',
                                                string='Expense Account Types', domain="[('type','=', 'other')]")

    @api.model
    def _verify_fiscalyear_last_day(self, company_id, last_day, last_month):
        company = self.browse(company_id)
        last_day = last_day or (company and company.fiscalyear_last_day) or 31
        last_month = last_month or (company and company.fiscalyear_last_month) or 12
        current_year = datetime.now().year
        last_day_of_month = calendar.monthrange(current_year, last_month)[1]
        return last_day > last_day_of_month and last_day_of_month or last_day

    @api.multi
    def compute_fiscalyear_dates(self, date):
        """ Computes the start and end dates of the fiscalyear where the given 'date' belongs to
            @param date: a datetime object
            @returns: a dictionary with date_from and date_to
        """
        self = self[0]
        last_month = self.fiscalyear_last_month
        last_day = self.fiscalyear_last_day
        if (date.month < last_month or (date.month == last_month and date.day <= last_day)):
            date = date.replace(month=last_month, day=last_day)
        else:
            if last_month == 2 and last_day == 29 and (date.year + 1) % 4 != 0:
                date = date.replace(month=last_month, day=28, year=date.year + 1)
            else:
                date = date.replace(month=last_month, day=last_day, year=date.year + 1)
        date_to = date
        date_from = date + timedelta(days=1)
        if date_from.month == 2 and date_from.day == 29:
            date_from = date_from.replace(day=28, year=date_from.year - 1)
        else:
            date_from = date_from.replace(year=date_from.year - 1)
        return {'date_from': date_from, 'date_to': date_to}

    @api.multi
    def _check_lock_dates(self, vals):
        super(ResCompany, self)._check_lock_dates(vals)
        prec_acc = self.env['decimal.precision'].precision_get('Account')

        if vals.get('fiscalyear_lock_date'):
            if self.env['account.move'].search_count([('date', '<=', vals['fiscalyear_lock_date']),
                                                      ('state', '=', 'draft')]):
                raise ValidationError(_('The account moves earlier than closing period date must be posted'))

            data = vals['fiscalyear_lock_date'].split('-')
            month = int(data[1])
            day = int(data[2])
            if month == self.fiscalyear_last_month and day == self.fiscalyear_last_day:
                nominal_accounts = self.env['account.account'].search([('user_type_id', 'in',
                                   self.income_account_type_ids.ids + self.expense_account_type_ids.ids)])
                if nominal_accounts:
                    account_values = \
                    self.env['report.account.report_trialbalance']._get_accounts(nominal_accounts, 'all')

                    for account_value in account_values:
                        if not float_is_zero(account_value['balance'], precision_digits=prec_acc):
                            raise ValidationError(_('There exist nominal accounts with balance'))

