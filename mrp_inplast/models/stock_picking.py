from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def add_sscc(self):
        partner = self.partner_id or self.parent_id.partner_id  # Obtener el partner

        for line in self.move_line_ids:
            if line.lot_id:
                # Generar y asignar SSCC1
                line.lot_id.with_context(sscc_field="sscc").get_next_sscc()
                print(
                    f"SSCC1 generado para el lote {line.lot_id.name}: {line.lot_id.sscc}"
                )

                # Si el partner tiene marcado el checkbox de "Generar dos SSCC", también generar SSCC2
                if partner.sscc_double:
                    line.lot_id.with_context(sscc_field="sscc2").get_next_sscc()
                    print(
                        f"SSCC2 generado para el lote {line.lot_id.name}: {line.lot_id.sscc2}"
                    )

        return True
