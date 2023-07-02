# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def _post_validate(self):
        for move in self:
            if move.line_ids:
                if not all([x.company_id.id == move.company_id.id for x in move.line_ids]):
                    raise UserError(_("Cannot create moves for different companies."))
        
        self.assert_balanced()

        self._check_lock_date()

        amount = 0.0
        balance = 0.0
        
        for line in self.line_ids:
            if line.account_id.internal_type == "liquidity":
                line_amount = 0.0
                line_account_balance = 0.0

                balance_field = 'aml.balance' if (not self.journal_id.currency_id or self.journal_id.currency_id == self.journal_id.company_id.currency_id) else 'aml.amount_currency'
            
                query = """SELECT sum(%s) FROM account_move_line aml
                        LEFT JOIN account_move move ON aml.move_id = move.id
                        WHERE aml.account_id in %%s
                        AND move.date <= %%s AND move.state = 'posted';""" % (balance_field,)
            
                self.env.cr.execute(query, (tuple(ac for ac in [line.account_id.id] if ac), fields.Date.context_today(self.journal_id),))
            
                query_results = self.env.cr.dictfetchall()
            
                if query_results and query_results[0].get('sum') != None:
                    line_account_balance = query_results[0].get('sum')

                line_amount = line.debit
                line_amount -= line.credit

                line_account_liquidity = line_account_balance + line_amount

                if line_account_liquidity < 0:
                    raise UserError("No es posible realizar esta transacción pues no se cuenta con suficiente balance contable.")

                amount += line_amount
                balance += line_account_balance

        liquidity = balance + amount
                
        if liquidity < 0:
            raise UserError("No es posible realizar esta transacción pues no se cuenta con suficiente balance contable.")
        
        return True

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _order = 'date desc, balance desc'
