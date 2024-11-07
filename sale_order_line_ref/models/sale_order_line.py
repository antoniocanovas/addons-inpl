# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 ForgeFlow S.L. (https://forgeflow.com)
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from datetime import timedelta

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    client_order_ref = fields.Char("Ref", help="Client Reference")

    def write(self, vals):
        res = super().write(vals)
        moves_to_upd = set()
        if "client_order_ref" in vals:
            for move in self.move_ids:
                if move.state not in ["cancel", "done"]:
                    moves_to_upd.add(move.id)
        if moves_to_upd:
            self.env["stock.move"].browse(moves_to_upd).write(
                {"client_order_ref": vals.get("client_order_ref")}
            )
        return res

    def _compute_customer_lead(self):
        super(SaleOrderLine, self)._compute_customer_lead()
        self.order_id._onchange_client_order_ref()
