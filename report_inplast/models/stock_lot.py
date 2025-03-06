from odoo import models, fields, api


class StockLot(models.Model):
    _inherit = "stock.lot"


    last_printed_label = fields.Integer(string="last printed label", default=0)
