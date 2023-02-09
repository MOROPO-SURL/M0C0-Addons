from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
    _inherit = 'validate.account.move'

    def _compute_account_moves_to_post(self):
        context = dict(self._context or {})
        domain_moves = [('state', '=', 'draft')]
        if context.get('active_model', False) == 'account.move':
            domain_moves.append(('id', 'in', context.get('active_ids')))
        elif context.get('active_model', False) == 'account.journal':
            domain_moves.append(('journal_id', 'in', context.get('active_ids')))
        return self.env['account.move'].search(domain_moves)

    account_move_ids = fields.Many2many('account.move', 'validate_account_move_rel',
                                        default=_compute_account_moves_to_post)
    account_moves_count = fields.Integer(compute='_compute_account_moves_count')

    @api.one
    @api.depends('account_move_ids')
    def _compute_account_moves_count(self):
        self.account_moves_count = len(self.account_move_ids)

    @api.multi
    def validate_move(self):
        move_to_post = self.env['account.move']
        for move in self.account_move_ids:
            if move.state == 'draft':
                move_to_post += move
        if not move_to_post:
            raise UserError(_('There is no journal items in draft state to post.'))
        move_to_post.post()
        return {'type': 'ir.actions.act_window_close'}