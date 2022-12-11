from odoo import models, api, _

class M0C0ChangeLockDate(models.Model):
    _id = "m0c0.change.lock.date"
    _inherit = "change.lock.date"

    def button_perform_backup(self):
        self.env.ref('auto_backup.action_server_backup').run()