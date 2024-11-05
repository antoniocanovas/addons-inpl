from odoo import _, api, fields, models

class ProductPacking(models.Model):
    _inherit = "product.packaging"

    mrp_bom_template_id = fields.Many2one("BOM template")
