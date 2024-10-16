from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_template_report(self):
        return "report_inplast.pnt_report_sale"
