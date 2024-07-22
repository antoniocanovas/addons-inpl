from odoo import models, fields, api

class PickingReportType(models.Model):
    _name = 'picking.report.type'
    _description = 'Customer can define diferent picking formats'


    name = fields.Char("Delivery slip name")
    coa = fields.Boolean("Attach COA")
    coa_handle = fields.Boolean("Attach COA Handle")
    coa_batch_certificate = fields.Boolean("Attach COA batch certificate")
    components_table = fields.Boolean("Attach Components table")