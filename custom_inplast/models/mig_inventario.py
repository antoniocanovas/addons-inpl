# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MigArticuloIdioma(models.Model):
    _name = 'mig.articuloidioma'
    _description = 'MIG Articulo Idioma'

    name = fields.Char('Producto')
    almacen = fields.Char('Almacén')
    ubicacion = fields.Char('Ubicación')
    lote = fields.Char('Lote')
    lotefecha = fields.Date('LoteFecha')
    sscc1 = fields.Char('sscc1')
    sscc2 = fields.Char('sscc2')
    palet = fields.Char('Palet')
    sil_id = fields.Many2one('stock.inventory.line', string='SIL')
