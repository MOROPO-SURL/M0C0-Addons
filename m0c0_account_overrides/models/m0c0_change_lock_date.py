from odoo import models, _
from odoo.exceptions import UserError

class M0C0ChangeLockDate(models.Model):
    _inherit = "change.lock.date"

    def button_perform_backup(self):
        self.env.ref('auto_backup.action_server_backup').run()