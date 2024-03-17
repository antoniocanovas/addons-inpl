# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class Migembalaje(models.Model):
    _name = 'mig.embalaje'
    _description = 'MIG embalaje'

    name = fields.Char('Embalaje (name)')
    producto = fields.Char('producto')
    cantidad = fields.Float('cantidad')
    cajapalet = fields.Char('cajapalet')
    escaja = fields.Boolean('escaja')