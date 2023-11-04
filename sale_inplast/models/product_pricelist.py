from odoo import _, api, fields, models
from datetime import date

import logging
_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread', 'mail.activity.mixin']


    # Productos en la lista de precios, para ser usados como los únicos a utilizar en ventas y facturas:
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

    # Productos utilizados como materia prima en las categorías de producto:
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


    # Crear una nota con los precios que han cambiado en la tarifa, desde botón o acción planificada:
    def pricelist_update_tracking(self):
        item_tracking = ""
        now = date.today()

        for li in self.item_ids:
            if (li.pnt_new_price != li.fixed_price):
                name = li.product_tmpl_id.name
                if li.product_id.id: name = li.product_id.name
                item_tracking += "<p>" + name + \
                                 ", Previous price: " + str(li.fixed_price) + \
                                 ", New price: " + str(li.pnt_new_price) + \
                                 "</p>"
                li.write({'pnt_tracking_date':now, 'fixed_price':li.pnt_new_price})

        if item_tracking != "":
            new_note = self.env['mail.message'].create({'body': item_tracking,
                                                        'message_type': 'comment',
                                                        'model': 'product.pricelist',
                                                        'res_id': self.id,
                                                        })

    # Recalcular precios de tarifa en base a parámetros establecidos:
    def products_pricelist_recalculation(self):
        for li in self.item_ids:
            product = li.product_tmpl_id
            categ = product.categ_id
            fault_percent = categ.pnt_mrp_fault_percent
            last_price = li.fixed_price
            raw_product = categ.pnt_material_type

            # Utilizo el campo de precio de venta para indicar el incremento para recálculo de tarifa:
            raw_increment = raw_product.list_price

            # Buscar la tarifa/peso en el producto, y si no existe en la familia:
            pricelist_weight = product.pnt_pricelist_weight
            if pricelist_weight == 0:
                pnt_pricelist_weight = product.categ_id.pnt_pricelist_weight

            # Incremento de precio debido al coste de materia prima (se consideran defectuosos):
            net_price = pricelist_weight * (raw_increment / 1000) * (1 + fault_percent/100) + (last_price * 1000)

            increment1 = net_price * (raw_product.pnt_i1 / 100)
            increment2 = pricelist_weight * (raw_product.pnt_i2 / 1000) * (1 + fault_percent/100)
            price1000 = net_price + increment1 + increment2 + raw_product.pnt_i3
            unit_price = price1000 / 1000
            li.write({'pnt_new_price':unit_price, 'pnt_tracking_date':date.today()})
