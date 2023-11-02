from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']

    @api.depends('item_ids.product_tmpl_id')
    def _get_pricelist_products(self):
        products = []
        product_categs = self.env['product.category'].search([('pnt_material_type','!=',False)])
        for li in product_categs:
            if (li.pnt_material_type.id) not in products:
                products.append(li.pnt_material_type.id)
        self.pnt_raw_product_ids = [(6,0,products)]
    pnt_raw_product_ids = fields.Many2many('product.template', store=False, compute='_get_pricelist_products')

    pnt_margin1_percent = fields.Float('Margin1 (%)', store=True, copy=False)
    pnt_margin2_percent = fields.Float('Margin2 (%)', store=True, copy=False)
    pnt_margen3_amount  = fields.Float('Margin3 (€)', store=True, copy=False)

    def products_pricelist_recalculation(self):
        return True
