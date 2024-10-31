# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MigCrearpacking(models.Model):
    _name = 'mig.crearpacking'
    _description = 'MIG Crear packings'

    # Campos de importación:
    name = fields.Char('Producto')
    mrp_type = fields.Char('mrp_type')
    sufix = fields.Float('sufix')
    box_base_qty = fields.Integer('box_base_qty')
    pallet_base_qty = fields.Float('pallet_base_qty')
    # Campos de control:
    pallet_id = fields.Many2one('product.template', string="pallet_id")
    box_id = fields.Many2one('product.template', string="box_id")