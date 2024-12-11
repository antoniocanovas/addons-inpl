from odoo import fields, models, api


class ProductCustomerCode(models.Model):
    _name = "product.customer.code"
    _description = "Product Customer Code"

    name = fields.Char(string="Name", required=1)
    partner_id = fields.Many2one('res.partner', string="Customer", required=1)
    product_tmpl_id = fields.Many2one('product.template', string="Product")