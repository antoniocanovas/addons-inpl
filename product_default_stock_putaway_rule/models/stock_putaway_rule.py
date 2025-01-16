# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class StockPutawayRule(models.Model):
    _inherit = "stock.putaway.rule"

    name = fields.Char('Name', store=True, compute='_get_name')
    @api.depends('product_id','location_in_id','location_out_id')
    def _get_name(self):
        for record in self:
            name = ""
            if record.id:
                name = "From: " + record.location_in_id.name + " to: " + record.location_out_id.name
            if record.product_id.id:
                name = record.product_id.name + " " + name
            record['name'] = name