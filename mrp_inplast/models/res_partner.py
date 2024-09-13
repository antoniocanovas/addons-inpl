from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    sscc_double = fields.Boolean(
        string="Generar dos SSCC",
        help="Si está marcado, se generarán SSCC1 y SSCC2. De lo contrario, solo SSCC1.",
    )
