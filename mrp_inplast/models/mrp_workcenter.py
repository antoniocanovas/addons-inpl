from odoo import _, api, fields, models

class ProductBomTemplate(models.Model):
    _inherit = "mrp.workcenter"

    power_kw = fields.Float("Power consumption (kw)")
