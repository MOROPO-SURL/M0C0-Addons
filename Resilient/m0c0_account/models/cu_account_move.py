# -*- coding: utf-8 -*-

from odoo import models, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _order = 'date desc, balance desc'
