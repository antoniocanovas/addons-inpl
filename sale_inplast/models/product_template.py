from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pnt_pricelist_weight = fields.Float('Pricelist weight', store=True, copy=True)
    pnt_margin1_percent = fields.Float('Margin1 (%)', store=True, copy=False)
    pnt_margin2_percent = fields.Float('Margin2 (%)', store=True, copy=False)
    pnt_margen3_amount  = fields.Float('Margin3 (€)', store=True, copy=False)
