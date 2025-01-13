# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "stock.move"

    client_order_ref = fields.Char("Ref", help="Client Reference")
