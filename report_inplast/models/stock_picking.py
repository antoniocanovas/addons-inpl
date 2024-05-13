from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def get_template_report(self):
        return self.partner_id.pnt_picking_report_id.xml_id