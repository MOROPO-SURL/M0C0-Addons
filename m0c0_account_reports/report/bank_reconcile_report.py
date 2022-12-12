# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class BankReconcileReport(models.AbstractModel):
    _name = 'report.m0c0_account_reports.bank_reconcile_report_view'

    def _compute_currency(self, journal_id, reconcile_date, amount):
        currency_id = ''
        if not journal_id.currency_id:
            currency_id = journal_id.company_id.currency_id
        elif journal_id.currency_id != journal_id.company_id.currency_id:
            currency_id = currency_id.with_context(date=reconcile_date)
        else:
            currency_id = journal_id.currency_id
        amount_currency = currency_id.compute(amount, currency_id)
        return amount_currency

    def _get_account_move_line_ids(self, move_state, journal_id, reconcile_date, sort_selection):
        account_move_line = {}
        params = [tuple(move_state), journal_id.id, reconcile_date]
        query = """
                  SELECT 
                      aml.id,
                      aml.ref,
                      aml.credit,
                      aml.debit,
                      aml.currency_id,
                      aml.date,
                      am.name

                  FROM
                      account_move am, 
                      account_account acc,
                      account_move_line aml,
                      account_journal aj


                  WHERE
                      aml.account_id = acc.id AND
                      acc.id = aj.default_account_id AND 
                      aml.move_id = am.id AND 
                      am.state in %s AND 
                      aml.journal_id = %s AND
                      aml.date <= %s AND
                      aml.statement_line_id is null

                  ORDER BY


                      """
        if sort_selection == 'date':
            query += 'aml.date'
        else:
            query += 'am.name'
        query += ', aml.move_id, acc.code'
        self.env.cr.execute(query, params)
        account_move_line.setdefault('+', [])
        account_move_line.setdefault('-', [])
        res = self.env.cr.fetchall()
        line_values = {rec[0]: (rec[1], rec[2], rec[3], rec[4], rec[5], rec[6]) for rec in res}
        for line in line_values:
            if line_values[line][1] > 0:
                line_amount = line_values[line][1]
                line_type = '-'

            if line_values[line][2] > 0:
                line_amount = line_values[line][2]
                line_type = '+'

            amount_currency = self._compute_currency(journal_id, reconcile_date, line_amount)
            account_move_line[line_type].append({
                'ref': line_values[line][0],
                'date': line_values[line][4],
                'number': line_values[line][5],
                'amount': amount_currency,
                'line_type': line_type,
                'credit': line_values[line][1],
                'debit': line_values[line][2],
            })
        return account_move_line

    def _get_account_move_line_fictions_ids(self, move_state, journal_id, reconcile_date,
                                           sort_selection):
        account_move_line_fictions = {}
        params = [journal_id.id, reconcile_date, reconcile_date]
        query = """SELECT 
             error.ref,
             error.date, 
             error.amount,
             correction.date AS dc 
           FROM 
             (public.account_bank_statement bs inner join
             public.account_bank_statement_line_fictions error on bs.id = error.statement_id)  left join 
             public.account_bank_statement_line_fictions correction on error.correction_id = correction.id
           WHERE 
             bs.journal_id = %s AND
             error.line_type = 'error' AND
             error.date <= %s AND
             (correction.date is null OR correction.date > %s )
           ORDER BY

                      """
        if sort_selection == 'date':
            query += 'error.date'
        else:
            query += 'error.ref'
        # query += ', aml.move_id, acc.code'
        self.env.cr.execute(query, params)
        account_move_line_fictions.setdefault('+', [])
        account_move_line_fictions.setdefault('-', [])
        for line in self.env.cr.fetchall():
            if line[2] < 0:
                line_amount = line[2]
                line_type = '-'

            if line[2] > 0:
                line_amount = line[2]
                line_type = '+'

            amount_currency = self._compute_currency(journal_id, reconcile_date, line_amount)

            account_move_line_fictions[line_type].append({
                'ref': line[0],
                'date': line[1],
                'amount': amount_currency,
                'line_type': line_type,
            })
            return account_move_line_fictions

    def _get_subtotal(self, data):
        subtotal = 0
        for m in data:
            subtotal += m['amount']
        return subtotal

    def _get_accounts(self, accounts, display_account):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        tables = tables.replace('"','')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts
        request = ("SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" +\
                   " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (not currency.is_zero(res['debit']) or not currency.is_zero(res['credit'])):
                account_res.append(res)
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        journal_id = self.env['account.journal'].browse(data['form']['journal_id'])
        reconcile_date = data['form']['reconcile_date']
        sort_selection = data['form']['sort_selection']
        target_move = data['form']['target_move']
        move_state = ['draft', 'posted']
        credit_subtotal = 0
        debit_subtotal = 0
        account_balance = 0
        line_amount = 0
        line_type = ''

        balance = self._get_accounts(journal_id.default_account_id, 'all')

        for acc in balance:
            account_balance = abs(self._compute_currency(journal_id, reconcile_date, acc['balance']))

        if target_move == 'posted':
            move_state = ['posted']


        # total_balance = account_balance + debit_subtotal - credit_subtotal

        accounts_move_line = self._get_account_move_line_ids(move_state, journal_id, reconcile_date, sort_selection)
        #accounts_move_line_fictions = self._get_account_move_line_fictions_ids(move_state, journal_id, reconcile_date, sort_selection)
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'company_id': journal_id.company_id.name,
            'reconcile_date': reconcile_date,
            'account_balance': account_balance,
            'total_balance': 0,
            'accounts_move_line': accounts_move_line,
            'accounts_move_line_fictions': [],
            'get_subtotal': self._get_subtotal,
        }

