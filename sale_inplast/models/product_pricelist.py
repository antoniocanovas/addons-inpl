from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']


    @api.depends('item_ids.product_tmpl_id')
    def _get_pricelist_products(self):
        products = []
        for li in self.item_ids:
            if (li.product_tmpl_id.id) and not (li.product_id.id):
                product_ids = self.env['product.product'].search([('product_tmpl_id', '=', li.product_tmpl_id.id)])
                for pro in product_ids: products.append(pro.id)
            else:
                products.append(li.product_id.id)
        self.product_ids = [(6,0,products)]
    product_ids = fields.Many2many('product.product', store=True, compute='_get_pricelist_products')


    @api.depends('item_ids.product_tmpl_id')
    def _get_raw_products(self):
        products = []
        product_categs = self.env['product.category'].search([('pnt_material_type','!=',False)])
        for li in product_categs:
            if (li.pnt_material_type.id) not in products:
                products.append(li.pnt_material_type.id)
        self.pnt_raw_product_ids = [(6,0,products)]
    pnt_raw_product_ids = fields.Many2many('product.template', string='Raw products', store=False,
                                           compute='_get_raw_products')


    def products_pricelist_recalculation(self):
        return True
