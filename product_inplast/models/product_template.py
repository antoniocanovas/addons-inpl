# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

LABELS = [
    ("standard", "Standard"),
    ("double", "Double"),
    ("sb", "San Bernardo"),
    ("buxton", "Buxton"),
    ("nestle", "Nestle"),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Tipo de productos en subfamilia:
    pnt_product_type = fields.Selection(
        [
            ("final", "End-product"),
            ("semi", "Semi-finished"),
            ("packing", "Packing"),
            ("raw", "Raw"),
            ("dye", "Dye"),
            ("packaging", "Packaging"),
            ("box", "Box"),
            ("pallet", "Pallet"),
            ("tool", "Tool"),
            ("other", "Other"),
        ],
        store=True,
        copy=True,
        string="MRP type",
    )
    pnt_parent_id = fields.Many2one("product.template", string="Main product")
    pnt_parent_qty = fields.Integer("Parent qty")
    pnt_product_dye = fields.Char(string="Product dye", store=True, copy=True)
    pnt_box_qty = fields.Integer("Box quantity")
    # ELIMINADO PARA TRABAJAR CON OCA MAYO 2024:
    #    @api.onchange('categ_id', 'pnt_parent_id', 'pnt_parent_qty', 'pnt_product_type')
    #    def _get_pnt_plastic_weight(self):
    #        for record in self:
    #            weight = record.categ_id.pnt_plastic_weight
    #            if record.pnt_product_type == 'packing':
    #                weight = record.pnt_parent_id.categ_id.pnt_plastic_weight * record.pnt_parent_qty
    #            record['pnt_plastic_weight'] = weight

    pnt_product_coa = fields.Many2one(
        "pnt.coa",
        string="COA",
    )
    pnt_label_type = fields.Selection(
        selection=LABELS, string="Label type", default="standard"
    )

    pnt_customer_code_print = fields.Boolean("Customer code on label")
    pnt_customer_code = fields.Char("Customer code")
    number_of_labels = fields.Integer(
        string="Number of labels", required=False, default="1"
    )

    @api.depends("name", "default_code", "pnt_product_dye")
    def _compute_display_name(self):
        for template in self:
            template.display_name = "{}{}{}".format(
                template.default_code and "[%s] " % template.default_code or "",
                template.name,
                template.pnt_product_dye and " [%s]" % template.pnt_product_dye or "",
            )

    pnt_pricelist_item_ids = fields.One2many(
        "product.pricelist.item", "product_tmpl_id", string="Pricelist items"
    )
    pnt_packing_ids = fields.One2many(
        "product.template", "pnt_parent_id", string="Packing products"
    )
    pnt_bom_line_ids = fields.One2many(
        "mrp.bom.line", "product_tmpl_id", string="BOM lines"
    )

    pnt_code = fields.Selection(
        [
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
            ("d", "D"),
            ("e", "E"),
            ("f", "F"),
            ("g", "G"),
            ("h", "H"),
            ("i", "I"),
            ("j", "J"),
            ("k", "K"),
            ("l", "L"),
            ("m", "M"),
            ("n", "N"),
            ("o", "O"),
            ("p", "P"),
            ("q", "Q"),
            ("r", "R"),
            ("s", "S"),
            ("t", "T"),
            ("u", "U"),
            ("v", "V"),
            ("w", "W"),
            ("x", "X"),
            ("y", "Y"),
            ("z", "Z"),
        ]
    )

    @api.depends(
        "pnt_code", "categ_id.pnt_code", "categ_id.parent_id.pnt_code", "bom_ids.code"
    )
    def _get_inplast_default_code(self):
        if self.pnt_product_type == "final":
            code = ""
            if self.categ_id.parent_id.pnt_code:
                code += self.categ_id.parent_id.pnt_code
            if self.categ_id.pnt_code:
                code += self.categ_id.pnt_code
            if self.pnt_code:
                code += self.pnt_code
            if self.bom_ids.ids:
                bom = self.bom_ids[0]
                if bom.code:
                    code += bom.code
            self.default_code = code

    default_code = fields.Char(compute="_get_inplast_default_code")
