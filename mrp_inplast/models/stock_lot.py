from odoo import models, fields, api

class StockLot(models.Model):
    _inherit = 'stock.lot'



    # Computed field to dynamically calculate product_id
    box_product_id = fields.Many2one(
        'product.product',
        compute='_compute_box_product_id',
        string="Box Product"
    )

    # Campo Many2many para las cajas relacionadas
    related_boxes_ids = fields.Many2many(
        'stock.lot',
        'stock_lot_related_boxes_rel',  # Explicit name for the relation table
        'lot_id',  # Column name for the current model (source)
        'related_lot_id',  # Column name for the target model
        string="Related Boxes",
        help="Boxes related to this lot.",
        domain="[('product_id', '=', box_product_id), ('parent_id', '=', id)]"
    )

    @api.depends('product_id')
    def _compute_box_product_id(self):
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
                    subproduct = self.env['product.product'].search([
                        ('pnt_product_type', '=', 'packing'),
                        ('id', 'in', record.product_id.pnt_parent_id.pnt_packing_ids.ids)
                    ], limit=1)
                    record.box_product_id = subproduct
                else:
                    record.box_product_id = False

    # Sobreescribe la función de mrp_lot_as_serial para tener en cuenta los lotes de cajas documentadas al fabricar palet:
    def update_lot_as_serial(self):
        # Son stock.move, buscamos sólo los que son tipo packing = palet del campo raw_move_ids:
        sms = self.env['stock.move'].search(
            [('id', 'in', self.move_raw_ids.ids), ('product_id.pnt_product_type', '=', 'packing')])
        boxeslot = []
        for sm in sms:
            if sm.move_line_ids.lot_id.related_boxes_ids:
                for li in sm.move_line_ids.lot_id.related_boxes_ids:
                    boxeslot.append(li.id)

        if not boxeslot:
            super().update_lot_as_serial()
        else:
            # Comprobar el número de lotes origen y destino, si no coinciden mensaje de error.
            # Asignar los lotes que ya existen a las cajas desmontadas.
            a = 0