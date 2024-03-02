# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class Migembalaje(models.Model):
    _name = 'mig.embalaje'
    _description = 'MIG embalaje'

    name = fields.Char('Embalaje')
    producto = fields.Char('Producto')
    cantidad = fields.Float('Cantidad')
    cajapalet = fields.Char('Caja/Palet')
