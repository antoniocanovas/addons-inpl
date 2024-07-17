from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def get_template_report(self):
        return "report_inplast.pnt_report_delivery_document"