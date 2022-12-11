from odoo import models, api, _

class M0C0ChangeLockDate(models.Model):
    _inherit = "change.lock.date"

    @api.multi
    def button_perform_backup(self):
        self.env.ref('auto_backup.action_server_backup').run()