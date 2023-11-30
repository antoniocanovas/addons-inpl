from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

#    pnt_product_ids = fields.Many2many('product.product', store=False, string='Pricelist products',
#                                   related='move_id.pricelist_id.pnt_product_ids')

    @api.depends('move_type', 'product_id')
    def _get_pnt_product_ids(self):
        for record in self:
            if (record.move_type in ['out_invoice','out_refund','out_receipt']):
                pp = move_id.pricelist_id.pnt_product_id
            elif (record.move_type in ['in_invoice','in_refund','in_receipt']):
                pp = self.env['product.product'].search([('purchase_ok','=',True)])
            else:  # Es 'entry'
                pp = self.env['product.product'].search([])
            record['pnt_product_ids'] = [(6, 0, pp.ids)]
    pnt_product_ids = fields.Many2many('product.product', store=False, string='Pricelist products',
