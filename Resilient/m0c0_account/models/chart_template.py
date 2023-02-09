# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    property_account_advance_receivable_id = fields.Many2one('account.account.template',
                                                             string='Account Advance Receivable')
    property_account_advance_payable_id = fields.Many2one('account.account.template', string='Account Advance Payable')

    @api.multi
    def generate_properties(self, acc_template_ref, company):
        super(AccountChartTemplate, self).generate_properties(acc_template_ref, company)

        self.ensure_one()
        
        PropertyObj = self.env['ir.property']
        
        todo_list = [
            ('property_account_advance_receivable_id', 'res.partner', 'account.account'),
            ('property_account_advance_payable_id', 'res.partner', 'account.account'),
        ]
        for record in todo_list:
            account = getattr(self, record[0])
            value = account and 'account.account,' + str(acc_template_ref[account.id]) or False
            if value:
                field = self.env['ir.model.fields'].search(
                    [('name', '=', record[0]), ('model', '=', record[1]), ('relation', '=', record[2])], limit=1)
                vals = {
                    'name': record[0],
                    'company_id': company.id,
                    'fields_id': field.id,
                    'value': value,
                }
                properties = PropertyObj.search([('name', '=', record[0]), ('company_id', '=', company.id)])
                if properties:
                    # the property exist: modify it
                    properties.write(vals)
                else:
                    # create the property
                    PropertyObj.create(vals)

        return True