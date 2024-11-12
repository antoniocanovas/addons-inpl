from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    client_order_ref = fields.Char(
        string="Ref",
        related="sale_line_ids.client_order_ref",
        store=True,
        help="Client Reference",
    )
