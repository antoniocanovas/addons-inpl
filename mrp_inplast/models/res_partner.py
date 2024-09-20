from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    sscc_qty = fields.Integer(
        string="Generar dos SSCC",
        help="Number of SSCC needed",
    )
