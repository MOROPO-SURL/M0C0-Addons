# -*- coding: utf-8 -*-

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def message_subscribe_users(self, user_ids=None, subtype_ids=None):
        if user_ids is None:
            user_ids = [self._uid]
        
        return self.message_subscribe(self.env['res.users'].browse(user_ids).sudo().mapped('partner_id').ids, subtype_ids=subtype_ids)
