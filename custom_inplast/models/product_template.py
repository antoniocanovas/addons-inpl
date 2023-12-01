# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"


    pnt_product_type = fields.Selection(string='Product type', related='categ_id.pnt_product_type')

    pnt_product_coa = fields.Many2one(
        "pnt.coa",
        string="COA",
    )
