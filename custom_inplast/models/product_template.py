# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"


    pnt_product_type = fields.Selection([('final','End-product'),
                                         ('semi', 'Semi-finished'),
                                         ('raw', 'Raw'),
                                         ('dye', 'Dye'),
                                         ('packing', 'Packing'),
                                         ('other', 'Other')],
                                        string='Product type', related='categ_id.pnt_product_type')
    pnt_product_dye_id = fields.Many2one('product.template', string='Product dye', store=True, copy=True)

    pnt_product_coa = fields.Many2one(
        "pnt.coa",
        string="COA",
    )
