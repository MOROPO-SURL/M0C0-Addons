# -*- coding: utf-8 -*-

from odoo import api, models, fields
from email.utils import formataddr


class Partner(models.Model):
    _inherit = 'res.partner'

    municipality = fields.Many2one('res.country.state.municipality', 'Municipio')
    short_name = fields.Char('Alias')

    @api.depends('name', 'email')
    def _compute_email_formatted(self):
        for partner in self:
            partner.email_formatted = formataddr((partner.name or u"False", partner.email or u"False"))

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        
        domain = []
        
        if name:
            domain = ['|', '|', ('name', operator, name), ('short_name', operator, name)]
        
        pos = self.search(domain + args, limit=limit)
        
        return pos.name_get()

    @api.multi
    def _display_address(self, without_company=False):
        address_format = self.country_id.address_format or \
                         self._get_default_address_format()
        args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'company_name': self.commercial_company_name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        args['municipality'] = self.municipality.name or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:
            return {'domain': {'municipality': [('state_id', '=', self.state_id.id)]}}
        else:
            return {'domain': {'municipality': []}}

    @api.onchange('municipality')
    def onchange_municipality_id(self):
        if self.municipality and len(self.municipality.state_id) > 0:
            self.state_id = self.municipality.state_id

    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id != self.municipality.state_id and self.municipality:
            self.municipality = ""
        if self.state_id and self.state_id != "":
            self.country_id = self.state_id.country_id

    @api.onchange('country_id')
    def onchange_country_id(self):
        if self.country_id != self.state_id.country_id and len(self.state_id.country_id) > 0:
            self.state_id = ""