from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pnt_pricelist_weight = fields.Float('Pricelist weight', store=True, copy=True)
    # falta el campo para el incremento de precio !!! usamos mientras el precio pvp