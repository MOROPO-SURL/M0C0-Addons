from odoo import models, api, _

class M0C0ChangeLockDate(models.TransientModel):
    _id = "m0c0.change.lock.date"
    _inherit = "change.lock.date"

    def button_perform_backup(self):
        self.env.ref('auto_backup.ir_cron_backup_scheduler_0_ir_actions_server').run()