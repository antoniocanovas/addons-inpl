from odoo import models, fields, api

class PickingReportType(models.Model):
    _name = 'picking.report.type'
    _description = 'Customer can define diferent picking formats'


    name = fields.Char("Delivery slip name")
    coa = fields.Boolean("Attach COA", default=True)
    coa_batch_certificate = fields.Boolean("Attach COA batch certificate")
    coa_multicolor = fields.Boolean("Attach COA Multicolor")
    coa_milk = fields.Boolean("Attach COA quality messures")
    coa_box_tracking = fields.Boolean("Attach box tracking")

