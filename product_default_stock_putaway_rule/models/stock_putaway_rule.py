# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class StockPutawayRule(models.Model):
    _inherit = "stock.putaway.rule"

    name = fields.Char('Name', compute='_get_name')
    def _get_name(self):
        for record in self:
            name = ""
            if record.id:
                name = "From: " + record.location_in_id.name + " to: " + record.location_out_id.name
            if record.product_id.id:
                name = record.product_id.name + " " + name
            record['name'] = name