from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def add_sscc(self):
        partner = self.partner_id or self.parent_id.partner_id  # Obtener el partner
        if partner.sscc_qty:
            qty = partner.sscc_qty
        else:
            qty = 1
        for line in self.move_line_ids:
            if line.lot_id:
                # Generar y asignar SSCC
                line.lot_id.get_next_sscc(qty)
        return True
