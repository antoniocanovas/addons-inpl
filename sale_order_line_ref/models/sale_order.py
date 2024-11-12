# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("client_order_ref")
    def _onchange_client_order_ref(self):

        for line in self.order_line:
            if not line.client_order_ref:
                line.client_order_ref = self.client_order_ref
