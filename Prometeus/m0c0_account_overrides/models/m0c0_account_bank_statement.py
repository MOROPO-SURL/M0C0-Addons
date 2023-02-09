from odoo import models, _
from odoo.exceptions import UserError

class M0C0AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    def button_reopen(self):
        raise UserError(_("Operación no permitida según las normas cubanas de contabilidad."))