# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MrpProductTool(models.Model):
    _name = "mrp.product.tool"

    name = fields.Char(related='product_tmpl_id.name')


    # Datos de empresa de categoría de moldes y accesorios para usar en dominios de equipos:
#    def get_tool_categ(self):
#        self.pnt_mrp_tool_categ_id = self.env.company.pnt_mrp_tool_categ_id.id
    pnt_mrp_tool_categ_id = fields.Many2one('maintenance.equipment.category', store=False,
                                            default=lambda self: self.env.company.pnt_mrp_tool_categ_id)
    def get_accesory_categ(self):
        self.pnt_mrp_accesory_categ_id = self.env.company.pnt_mrp_accesory_categ_id.id
    pnt_mrp_accesory_categ_id = fields.Many2one('maintenance.equipment.category', store=False,
                                                compute='get_accesory_categ')

    def get_blade_categ(self):
        self.pnt_mrp_blade_categ_id = self.env.company.pnt_mrp_blade_categ_id.id
    pnt_mrp_blade_categ_id = fields.Many2one('maintenance.equipment.category', store=False,
                                                compute='get_blade_categ')

    # El molde para usar en la fabricación (con o sin accesorio):
    pnt_tool_id = fields.Many2one('maintenance.equipment', string='Mold', store=True, copy=True)
    pnt_accesory_id = fields.Many2one('maintenance.equipment', string='Accesory', store=True, copy=True)
    pnt_blade_id = fields.Many2one('maintenance.equipment', string='Blade', store=True, copy=True)

    pnt_accesory_ids = fields.Many2many(related="pnt_tool_id.pnt_tool_accesory_ids")
    pnt_blade_ids = fields.Many2many(related="pnt_tool_id.pnt_tool_blade_ids")
    product_tmpl_id = fields.Many2one('product.template', string='Product')