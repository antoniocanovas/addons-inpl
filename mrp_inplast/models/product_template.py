# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Datos de empresa de categoría de moldes y accesorios para usar en dominios de equipos:
    pnt_mrp_tool_categ_id = fields.Many2one('maintenance.equipment.category', store=False,
                                            compute=lambda self: self.env.company.pnt_mrp_tool_categ_id.id)
    pnt_mrp_accesory_categ_id = fields.Many2one('maintenance.equipment.category', store=False,
                                                compute=lambda self: self.env.company.pnt_mrp_accesory_categ_id.id)

    # El molde para usar en la fabricación (con o sin accesorio):
    pnt_tool_id = fields.Many2one('maintenance.equipment', string='Mold', store=True, copy=True)
