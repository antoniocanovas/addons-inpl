from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def get_template_report(self):
        return self.partner_id.pnt_sale_report_id.xml_id