# -*- coding: utf-8 -*-

from odoo import api, models, fields


class ResCountryMunicipality(models.Model):
    _description = "Municipio"
    _name = 'res.country.state.municipality'
    _order = 'code'
    _rec_name = 'name'

    state_id = fields.Many2one('res.country.state', 'State', required=True)
    name = fields.Char('Nombre del Municipio', size=64, required=True)
    code = fields.Char('Código del Municipio', size=3, required=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', string='Country', required=True)
    dpa_code = fields.Char('Código DPA', compute='_compute_dpa_code', store=True)

    @api.depends('state_id', 'code')
    def _compute_dpa_code(self):
        for municipality in self:
            if municipality.state_id and municipality.code:
                municipality.dpa_code = '%s%s' % (municipality.state_id.code, municipality.code)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if self.env.context.get('state_id'):
            args = args + [('state_id', '=', self.env.context.get('state_id'))]
        firsts_records = self.search([('code', '=ilike', name)] + args, limit=limit)
        search_domain = [('name', operator, name)]
        search_domain.append(('id', 'not in', firsts_records.ids))
        records = firsts_records + self.search(search_domain + args, limit=limit)
        return [(record.id, record.display_name) for record in records]

    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, code)', 'The code of the municipality must be unique by state !')
    ]
