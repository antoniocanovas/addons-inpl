from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    pnt_material_type = fields.Many2one('product.template', store=True, copy=True, domain="[('detailed_type','=','product')]")
    pnt_pricelist_weight = fields.Float('Pricelist weight', store=True, copy=True)
    pnt_mrp_fault_percent = fields.Float('Fault (%)', store=True, copy=True)




