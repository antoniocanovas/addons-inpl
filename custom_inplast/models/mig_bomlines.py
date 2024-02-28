# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MigBomlines(models.Model):
    _name = 'mig.bomlines'
    _description = 'MIG Bomlines'

    name = fields.Char('Componente')
    producto = fields.Char('Producto')
    cantidad = fields.Float('Cantidad')
