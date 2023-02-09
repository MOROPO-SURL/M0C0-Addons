# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    destination_type = fields.Selection([('obligation', 'Liquidación'), ('advance', 'Anticipado'), ('other', 'Other')],
                                        string='Tipo', required=True, default='obligation')
    other_destination_account_id = fields.Many2one('account.account', domain=[('deprecated', '=', False)],
                                                   default=lambda self: self.env.user.company_id.transfer_account_id.id)

    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id', 'destination_type', 'other_destination_account_id')
    def _compute_destination_account_id(self):
        if self.destination_type == 'advance':
            if self.partner_id:
                if self.partner_type == 'customer':
                    self.destination_account_id = self.partner_id.property_account_advance_receivable_id.id
                else:
                    self.destination_account_id = self.partner_id.property_account_advance_payable_id.id
            elif self.partner_type == 'customer':
                default_account = self.env['ir.property'].get('property_account_advance_receivable_id', 'res.partner')
                self.destination_account_id = default_account.id
            elif self.partner_type == 'supplier':
                default_account = self.env['ir.property'].get('property_account_advance_payable_id', 'res.partner')
                self.destination_account_id = default_account.id
        elif self.destination_type == 'other':
            self.destination_account_id = self.other_destination_account_id.id
        elif self.destination_type == 'obligation':
            super(AccountPayment, self)._compute_destination_account_id()

    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        val = super(AccountPayment, self)._onchange_payment_type()
        
        if self.payment_type == 'transfer':
            self.destination_type = 'obligation'
        
        return val

