# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api


class LedgerReport(models.AbstractModel):
    _name = 'report.m0c0_account.ledger_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        account_ids = data['form']['account_ids']
        target_move = data['form']['target_move']
        date_to = data['form']['date_to']
        date_data = date_to.split('-')
        year = date_data[0]
        month = date_data[1]
        day = date_data[2]
        docs = []
        where = []
        params = []
        row_number = int(month) > 6 and 2 or 1
        select = ["SUM(CASE WHEN to_char(p.date, 'YYYY-MM') < '%(year)s-01' THEN p.balance ELSE 0 END)"]
        for m in range(1, 13):
            current_month = str(m)
            if len(current_month) == 1:
                current_month = '0' + current_month
            field = "NULL"
            if current_month <= month:
                field = "SUM(CASE WHEN to_char(p.date, 'YYYY-MM') <= '%%(year)s-%s' THEN p.balance ELSE 0 END) " % current_month
            select.append(field)
        select.append("SUM(CASE WHEN p.date <= '%s' THEN p.balance ELSE 0 END)" % date_to)

        sql_select = ", ".join(select) % {'year': year}
        where.append("account_id in %s")
        if target_move == "posted":
            where.append("m.state = 'posted'")
        SQL = """
            SELECT p.account_id, %s
            FROM account_move_line as p, account_move m
            WHERE m.id = p.move_id
            AND %s
            
            
            group by p.account_id
            """ % (sql_select, " AND ".join(where))

        if len(account_ids) == 0:
            account_ids = self.env['account.account'].search([]).ids
        params.append(tuple(account_ids))

        self.env.cr.execute(SQL, params)

        account_obj = self.env['account.account']
        for line in self.env.cr.fetchall():
            docs.append({
                'code': account_obj.browse(line[0]).code,
                'account_id': account_obj.browse(line[0]).name,
                'initial': line[1],
                'january':  line[2],
                'february': line[3],
                'march': line[4],
                'april': line[5],
                'may': line[6],
                'june': line[7],
                'july': line[8],
                'august': line[9],
                'september': line[10],
                'october': line[11],
                'november': line[12],
                'december': line[13],
                'to_date': line[14],
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_to': date_to,
            'target_move': target_move,
            'accounts': account_ids,
            'docs': docs,
            'row_number': row_number,
        }
