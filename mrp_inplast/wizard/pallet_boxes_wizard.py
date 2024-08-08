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

    @api.onchange('pallet_id')
    def _onchange_pallet_id(self):
        """ Este método se ejecuta cuando cambia el campo 'pallet_id'. """
        if self.pallet_id:
            # Buscar todos los lotes con el parent_id igual a pallet_id
            lots = self.env['stock.lot'].search([('parent_id', '=', self.pallet_id.id)])
            # Asignar todos los lotes encontrados al campo many2many
            self.pnt_processed_barcodes = [(6, 0, lots.ids)]
        else:
            # Limpiar el campo si no hay un pallet_id seleccionado
            self.pnt_processed_barcodes = [(5, 0, 0)]

    @api.onchange('pnt_barcode_input')
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

                    # Buscar el subproducto con el campo pnt_product_type = 'box'
                    subproduct = self.env['product.product'].search([
                        ('pnt_product_type', '=', 'box'),
                        ('id', 'in', self.production_id.product_id.pnt_parent_id.pnt_packing_ids.ids)
                    ], limit=1)

                    if not subproduct:
                        raise UserError(_("No se encontró un subproducto con el tipo 'box'."))

                    for lot in lots:
                        lot_name = 'MO' + lot.strip()
                        # Busca si el lote ya existe
                        exist = self.env['stock.lot'].search(
                            [('name', '=', lot_name)])
                        if not exist:
                            # Si no existe, crea un nuevo lote
                            new_lot = self.env['stock.lot'].create({
                                'product_id': subproduct.id,
                                'name': lot_name,
                                'parent_id': self.pallet_id.id,
                            })
                            boxes.append(new_lot.id)
                        else:
                            # Si ya existe, añade el lote existente a la lista de boxes
                            boxes.append(exist.id)

                    # Asigna los códigos de barras procesados a 'pnt_processed_barcodes'

                    lots = self.env['stock.lot'].search([('parent_id', '=', self.pallet_id.id)])
                    record.pnt_processed_barcodes = [(6, 0, lots.ids)]

                    # Actualiza el campo many2many de cajas relacionadas en el lote correspondiente
                    if self.pallet_id:
                        lots = self.env['stock.lot'].search([('parent_id', '=', self.pallet_id.id)])
                        # Asignar todos los lotes encontrados al campo many2many
                        self.pallet_id.related_boxes_ids = [(6, 0, lots.ids)]

    def add_lots(self):
        # Este método se ejecuta cuando se hace clic en el botón "Add Lots".
        pass
