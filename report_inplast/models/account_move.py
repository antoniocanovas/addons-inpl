from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'


    def get_template_report(self):
        return self.partner_id.pnt_invoice_report_id.xml_id