from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_ids = fields.Many2many('product.product', store=False, string='Pricelist products',
                                   related='order_id.pricelist_id.product_ids')





