# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    property_account_advance_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                             string="Account Advance Receivable",
                                                             domain="[('internal_type', '=', 'payable'), "
                                                                    "('deprecated', '=', False)]",
                                                             help="This account will be used instead of the default one"
                                                                  " as the advance receivable account for the "
                                                                  "current partner", required=False)
    property_account_advance_payable_id = fields.Many2one('account.account', company_dependent=True,
                                                          string="Account Advance Payable",
                                                          domain="[('internal_type', '=', 'receivable'), ('deprecated',"
                                                                 " '=', False)]",
                                                          help="This account will be used instead of the default one as"
                                                               " the advance payable account for the current partner",
                                                          required=False)
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
                                                  string="Account Payable", oldname="property_account_payable",
                                                  domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=False)
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Account Receivable", oldname="property_account_receivable",
                                                     domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=False)
