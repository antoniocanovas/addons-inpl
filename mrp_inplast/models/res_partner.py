from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    number_sscc = fields.Integer(string="Numbers of SSCC")
