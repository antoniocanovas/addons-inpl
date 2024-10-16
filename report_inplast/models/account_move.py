from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    def get_template_report(self):
        return "report_inplast.pnt_report_invoice"
