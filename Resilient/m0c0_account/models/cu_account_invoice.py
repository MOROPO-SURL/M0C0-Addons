# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, Warning
from odoo.addons import decimal_precision as dp


class AccountInvoicePlus(models.Model):
    _inherit = 'account.invoice'

    other_partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account', readonly=True,
                                            states={'draft': [('readonly', False)]}, help='Bank Account Number to which'
                                            ' the invoice will be paid. A Company bank account if this is a Vendor Bill'
                                            ' or Customer Credit Note, otherwise a Partner bank account number.')
    operation = fields.Selection([('sale', 'Wholesale of goods and services.'),
                                 ('internal_sale', 'Internal sale where they mediate operations of collection and payments.'),
                                 ('delivery', 'Deliveries of products on consignment or in warehouses.'),
                                 ('active_sale', 'Sales of tangible fixed assets.'), ('return', 'Make returns.')],
                                 required=True, readonly=True, states={'draft': [('readonly', False)]}, default='sale',
                                 track_visibility='always')
    carrier_id = fields.Many2one('res.partner', string='Carrier', readonly=True,
                                      states={'draft': [('readonly', False)]}, domain=[('is_company', '=', False)],
                                      help="Person who carrier the invoice.")
    vehicle_plate = fields.Char(string='Vehicle plate', copy=False, readonly=True, states={'draft': [('readonly', False)]}
                                , help="The vehicle plate of the invoice carrier.")
    card_number = fields.Char(string='Freight Card Number', copy=False, readonly=True, states={'draft': [('readonly', False)]})
    railroad_locker = fields.Char(string='Railroad locker', copy=False, readonly=True, states={'draft': [('readonly', False)]})
    contract = fields.Char('Contract')
    contract_date = fields.Date('Contract Date')
    sheet_number = fields.Char('Sheet Number') # Folio
    date_invoice = fields.Date(string='Invoice Date',
                               readonly=True, states={'draft': [('readonly', False)]},
                               index=True,
                               help="Keep empty to use the current date", copy=False,
                               default=fields.Date.today())

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        warning = {}
        domain = {}
        company = self.company_id
        p = self.partner_id if not company else self.partner_id.with_context(force_company=company.id)
        type = self.type
        if p:
            rec_account = p.property_account_receivable_id
            pay_account = p.property_account_payable_id
            if not rec_account and not pay_account:
                action = self.env.ref('account.action_account_config')
                msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('out_invoice', 'out_refund'):
                account_id = rec_account.id
                payment_term_id = p.property_payment_term_id.id
            else:
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term_id.id

            delivery_partner_id = self.get_delivery_partner_id()
            fiscal_position = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id, delivery_id=delivery_partner_id)

            # If partner has no warning, check its company
            if p.invoice_warn == 'no-message' and p.parent_id:
                p = p.parent_id
            if p.invoice_warn != 'no-message':
                # Block if partner only has warning but parent company is blocked
                if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
                    p = p.parent_id
                warning = {
                    'title': _("Warning for %s") % p.name,
                    'message': p.invoice_warn_msg
                    }
                if p.invoice_warn == 'block':
                    self.partner_id = False

        self.account_id = account_id
        self.payment_term_id = payment_term_id
        self.date_due = False
        self.fiscal_position_id = fiscal_position

        if type in ('in_invoice', 'out_refund'):
            bank_ids = p.commercial_partner_id.bank_ids
            bank_id = bank_ids[0].id if bank_ids else False
            self.partner_bank_id = bank_id
            company_bank_ids = company.partner_id.commercial_partner_id.bank_ids
            company_bank_id = company_bank_ids[0].id if company_bank_ids else False
            self.other_partner_bank_id = company_bank_id
            domain = {'partner_bank_id': [('id', 'in', bank_ids.ids)],
                      'other_partner_bank_id': [('id', 'in', company_bank_ids.ids)]}
        else:
            bank_ids = company.partner_id.commercial_partner_id.bank_ids
            bank_id = bank_ids[0].id if bank_ids else False
            self.partner_bank_id = bank_id
            company_bank_ids = p.commercial_partner_id.bank_ids
            company_bank_id = company_bank_ids[0].id if company_bank_ids else False
            self.other_partner_bank_id = company_bank_id
            domain = {'partner_bank_id': [('id', 'in', bank_ids.ids)],
                      'other_partner_bank_id': [('id', 'in', company_bank_ids.ids)]}

        res = {}
        if warning:
            res['warning'] = warning
        if domain:
            res['domain'] = domain
        return res
