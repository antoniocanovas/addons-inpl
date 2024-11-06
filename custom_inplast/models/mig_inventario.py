# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MigArticuloIdioma(models.Model):
    _name = 'mig.articuloidioma'
    _description = 'MIG Articulo Idioma'

    name = fields.Char('Producto')
    ubicacion = fields.Char('ubicación')
    ubicacion_old = fields.Char('Ubicacion_old')
    lote = fields.Char('Lote')
    lotefecha = fields.Date('LoteFecha')
    sscc1 = fields.Char('sscc1')
    sscc2 = fields.Char('sscc2')
    palet = fields.Char('Palet')
    sil_id = fields.Many2one('stock.inventory.line', string='SIL')
