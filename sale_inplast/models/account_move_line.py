from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pnt_product_ids = fields.Many2many('product.product', store=False, string='Pricelist products',
                                   related='move_id.pricelist_id.pnt_product_ids')

    pnt_product_type = fields.Selection(related="product_id.pnt_product_type")
