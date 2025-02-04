# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MigInventario(models.Model):
    _name = 'mig.inventario'
    _description = 'MIG Inventario'

    name = fields.Char('Nombre Prod')
    ubicacion = fields.Char('ubicación')
    ubicacion_old = fields.Char('Ubicacion_old')
    lote = fields.Char('Lote')
    qty = fields.Float(string='qty')
    sscc1 = fields.Char('sscc1')
    sscc2 = fields.Char('sscc2')
    palet = fields.Char('Palet')

    lot_id = fields.Many2one('stock.lot', string='lot_id')
    product_id = fields.Many2one('product.product', string='Producto')
    location_id = fields.Many2one('stock.location', string='location')
    sml_id = fields.Many2one('stock.move.line', string='Stock move line')
    mig_fechafabricacion = fields.Date('Fecha fabricación')


    @api.model
    def _update_mig_inventario(self):
        # PROCEDIMIENTO:
        # 1. Los registros llegan a mig_inventario por creación manual o comunicación RPC desde sistema antiguo.
        # 2. Este método regulariza inventario automáticamente para los registros con ubicación y producto detectados.
        # Quedan excluídos los que ya han sido regularizados (tienen sml_id asignado).

        for r in self:
            lote, ssccs = False, []

            # Busco la ubicación:
            locationname = r.ubicacion.strip() + " (" + r.ubicacion_old.strip() + ")"
            location = self.env['stock.location'].search([('name', '=', locationname)])
            if len(location.ids) > 1: raise UserError('Varias ubicaciones con el mismo nombre: ' + locationname)

            # Busco el producto:
            productname = r.name.strip()
            product = self.env['product.product'].search([('default_code', '=', productname)])
            if len(product.ids) > 1: raise UserError('Varios productos con la misma referencia: ' + productname)

            # Crear lotes si no existen y actualizar inventario:
            if product.id and location.id and not r.sml_id.id:
                nombrelote = r.lote + "/" + r.palet
                lot = self.env['stock.lot'].search([('name', '=', nombrelote), ('product_id', '=', product.id)])
                if lot.ids:
                    lote = lot[0].id
                    # Cambiado 15/Enero/25 para considerar lotes que ya existen:
                    # raise UserError('El lote ya existe: ' + nombrelote)
                else:
                    ssccs, parentlotname = [], False
                    parentlotname = nombrelote.split(".")
                    parentlot = self.env['stock.lot'].search(
                        [('name', '=', parentlotname[0]), ('product_id', '=', product.id)])
                    if not parentlot.id and parentlotname:
                        parentlot = self.env['stock.lot'].create(
                            {'name': parentlotname[0], 'mig_fechafabricacion': r.mig_fechafabricacion,
                             'product_id': product.id})

                    if r.sscc1:
                        sscc1 = self.env['pnt.sscc.code'].create({'name': r.sscc1})
                        ssccs.append(sscc1.id)
                    if r.sscc2:
                        sscc2 = self.env['pnt.sscc.code'].create({'name': r.sscc2})
                        ssccs.append(sscc2.id)
                    lote = self.env['stock.lot'].create(
                        {'name': nombrelote, 'mig_fechafabricacion': r.mig_fechafabricacion, 'product_id': product.id,
                         'parent_id': parentlot.id, 'sscc_code_ids': [(6, 0, ssccs)]}).id

                # Procedimiento de inventariado automático:
                newsm = self.env['stock.move'].create(
                    {'name': product.name, 'product_id': product.id, 'location_id': 14, 'location_dest_id': location.id,
                     'product_uom_qty': r.qty, 'company_id': self.env.company.id, 'state': 'done'})
                newsml = self.env['stock.move.line'].create({
                    'product_id': product.id, 'location_id': 14, 'location_dest_id': location.id, 'qty_done': r.qty,
                    'company_id': self.env.company.id, 'lot_id': lote, 'move_id': newsm.id, 'state': 'done'})

                # Registrar línea mig_inventario:
                r.write({'product_id': product.id, 'location_id': location.id, 'lot_id': lote, 'sml_id': newsml.id})
