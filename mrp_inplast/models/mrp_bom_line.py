# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    pnt_raw_percent = fields.Float('Percent')
    pnt_raw_type_id = fields.Many2one(related='bom_id.pnt_raw_type_id')

    def write(self, vals):
        if "pnt_raw_percent" in vals:
            qty = self.product_qty
            if (vals["pnt_raw_percent"] != 0) and (
                    self.pnt_raw_type_id == self.product_uom_category_id):
                qty = self.bom_id.pnt_raw_qty * vals["pnt_raw_percent"] / 100
            vals['product_qty'] = qty
        super(MrpBomLine, self).write(vals)

    @api.onchange('pnt_raw_percent','product_id')
    def _get_uom_from_percent_type(self):
        for record in self:
            # Falta el if de que sea la misma clase de unidad y asginar la misma que del peso o volumen:
            uom = record._origin.product_uom_id
            if (record.pnt_raw_percent != 0) and (record.pnt_raw_type_id == record.product_uom_category_id):
                uom = record.env['uom.uom'].search([
                    ('category_id','=',record.product_uom_category_id.id),
                    ('uom_type','=','reference')
                ])
            record['product_uom_id'] = uom.id
    product_uom_id = fields.Many2one(compute='_get_uom_from_percent_type', store=True)