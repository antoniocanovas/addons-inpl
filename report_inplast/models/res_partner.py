from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #pnt_sale_report_id = fields.Many2one('ir.ui.view', domain=[("priority", "=", "20")])
    #pnt_invoice_report_id = fields.Many2one('ir.ui.view', domain=[("priority", "=", "21")])
    pnt_picking_report_id = fields.Many2one('picking.report.type')

    #pnt_label_box_type_id = fields.Many2one('ir.ui.view', domain=[("priority", "=", "23")])
    #pnt_label_pallet_type_id = fields.Many2one('ir.ui.view', domain=[("priority", "=", "24")])
