from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    container_type_id = fields.Many2one(related='sale_id.container_type_id')