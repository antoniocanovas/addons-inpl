from odoo import _, api, fields, models
from odoo.exceptions import UserError

class PalletBoxesWizard(models.TransientModel):
    _name = 'pallet.boxes.wizard'
    _description = 'Add boxes to Lot'

    production_id = fields.Many2one(
        'mrp.production', required=True,
        default=lambda self: self.env.context.get('production_id', None))
    lot_producing_id = fields.Many2one(related="production_id.lot_producing_id")
    pallet_id = fields.Many2one('stock.lot', string="Pallet", domain="[('parent_id', '=', lot_producing_id)]")
    pnt_barcode_input = fields.Text('Boxes read')
    pnt_processed_barcodes = fields.Many2many('stock.lot', string="Boxes")

    @api.onchange('boxes_barcode_string')
    def _onchange_pnt_barcode_input(self):
        # Este método se ejecuta cada vez que 'pnt_barcode_input' cambia.
        for record in self:
            if record.pnt_barcode_input:
                line = record.pnt_barcode_input
                lots, boxes = [], []

                if line:
                    # Divide la entrada del código de barras en lotes basados en 'MO'
                    lots = line.split('MO')
                    lots = [lot for lot in lots if lot]
                    for lot in lots:
                        lot_name = 'MO' + lot.strip()
                        # Busca si el lote ya existe
                        exist = self.env['stock.lot'].search(
                            [('name', '=', lot_name)])
                        if not exist:
                            # Si no existe, crea un nuevo lote
                            new_lot = self.env['stock.lot'].create({
                                'product_id': record.pnt_sub_product_id.id,
                                'name': lot_name,
                                'pnt_originating_product_id': record.product_id.id,
                                'pnt_originating_lot_id': record._origin.id
                            })
                            boxes.append(new_lot.id)
                        else:
                            # Si ya existe, añade el lote existente a la lista de boxes
                            boxes.append(exist.id)

                    # Asigna los códigos de barras procesados a 'pnt_processed_barcodes'
                    record.pnt_processed_barcodes = [(6, 0, boxes)]

    def add_lots(self):
        print("")