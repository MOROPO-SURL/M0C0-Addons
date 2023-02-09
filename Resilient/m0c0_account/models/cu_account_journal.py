
from odoo import api, models, _

class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'

    @api.multi
    def open_action_with_context_dashboard(self):
        action_name = self.env.context.get('action_name', False)
        
        if not action_name:
            return False
        
        ctx = dict(self.env.context, default_journal_id=self.id)
        ir_model_obj = self.env['ir.model.data']
        model, action_id = ir_model_obj.get_object_reference('m0c0_account', action_name)
        [action] = self.env[model].browse(action_id).read()
        action['context'] = ctx
        
        return action


