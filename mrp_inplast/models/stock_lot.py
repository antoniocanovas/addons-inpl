from odoo import models, fields, api
from gtin import GTIN


class StockLot(models.Model):
    _inherit = "stock.lot"

    # Computed field to dynamically calculate product_id
    box_product_id = fields.Many2one(
        "product.product", compute="_compute_box_product_id", string="Box Product"
    )

    # Campo Many2many para las cajas relacionadas
    related_boxes_ids = fields.Many2many(
        "stock.lot",
        "stock_lot_related_boxes_rel",  # Explicit name for the relation table
        "lot_id",  # Column name for the current model (source)
        "related_lot_id",  # Column name for the target model
        string="Related Boxes",
        help="Boxes related to this lot.",
        domain="[('product_id', '=', box_product_id), ('parent_id', '=', id)]",
    )
    invisible_fields = fields.Boolean(
        string="Invisible Fields",
    )
    sscc = fields.Char(string="SSCC1", help="SSCC1 number for the lot")
    sscc2 = fields.Char(string="SSCC2", help="SSCC2 number for the lot")

    def get_next_sscc(self):
        """Genera un SSCC completo sin usar la librería gtin."""
        if self.env.context.get("sscc_field") == "sscc" and self.sscc:
            return  # sscc1 is already filled, so we do not generate a new one
        if self.env.context.get("sscc_field") == "sscc2" and self.sscc2:
            return  # sscc2 is already filled, so we do not generate a new one

        seq = self.env["ir.sequence"].search([("code", "=", "pnt.sscc.code")], limit=1)
        pnt_extension_digit = seq.pnt_extension_digit
        SSCC = self.env["ir.sequence"].next_by_code("pnt.sscc.code")

        # Asegurarse de que el prefijo de empresa tiene una longitud válida
        if len(seq.prefix) < 7 or len(seq.prefix) > 10:
            raise ValueError(
                "El prefijo de la empresa debe tener entre 7 y 10 dígitos."
            )

        # Crear el SSCC sin el dígito de control
        # sscc_pre = str(pnt_extension_digit) + str(SSCC)

        sscc = (
            str(pnt_extension_digit) + str(SSCC) + str(GTIN(raw=str(SSCC)).check_digit)
        )
        # Generar el dígito de control usando el algoritmo de Luhn
        ##sscc = self.calculate_luhn(sscc_pre)

        # Asignar el SSCC a sscc1 o sscc2 dependiendo del contexto
        if self.env.context.get("sscc_field") == "sscc2":
            self.sscc2 = sscc
        else:
            self.sscc = sscc

    @api.depends("product_id")
    def _compute_box_product_id(self):
        invisible_fields = True
        for record in self:
            if record.product_id:
                matching_record = None

                for packing_record in record.product_id.pnt_parent_id.pnt_packing_ids:
                    pallet_qty = record.product_id.pnt_parent_qty
                    box_qty = record.product_id.pnt_box_qty
                    division = pallet_qty // box_qty
                    check_qty = packing_record.pnt_parent_qty
                    # Comprueba si la división es igual
                    if division == check_qty:
                        matching_record = packing_record
                        break  # Si encuentras un registro que cumple, puedes salir del bucle
                # Find the box product related to this lot's product
                if matching_record:
                    subproduct = self.env["product.product"].search(
                        [
                            ("pnt_product_type", "=", "packing"),
                            (
                                "id",
                                "in",
                                record.product_id.pnt_parent_id.pnt_packing_ids.ids,
                            ),
                        ],
                        limit=1,
                    )
                    record.box_product_id = subproduct
                    invisible_fields = (
                        matching_record.id == record.product_id.id
                        or record.parent_id.id == False
                    )

                else:
                    record.box_product_id = False
        record.invisible_fields = invisible_fields

    def action_open_stock_lot_boxes_wizard(self):
        return {
            "name": ("Add Boxes to Lot"),
            "type": "ir.actions.act_window",
            "res_model": "stock.lot.boxes.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_lot_id": self.id,
            },
        }