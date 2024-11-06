# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MigArticuloIdioma(models.Model):
    _name = 'mig.inventario'
    _description = 'MIG Inventario'

    name = fields.Char('Producto')
    ubicacion = fields.Char('ubicación')
    ubicacion_old = fields.Char('Ubicacion_old')
    lote = fields.Char('Lote')
    qty = fields.Float(string='qty')
    sscc1 = fields.Char('sscc1')
    sscc2 = fields.Char('sscc2')
    palet = fields.Char('Palet')

    lot_id = fields.Many2one('stock.lot', string='lot_id')
    product_id = fields.Many2one('product.product', string='pp')
    location_id = fields.Many2one('stock.location', string='location')
