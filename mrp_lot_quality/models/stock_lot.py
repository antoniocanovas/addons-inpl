# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class StockLot(models.Model):
    _inherit = "stock.lot"

    quality_meassure_line_ids = fields.One2many('quality.meassure.line', 'lot_id', string="Quality Meassure")

    def action_view_quality_meassure(self):
        action = self.env['ir.actions.act_window']._for_xml_id('mrp_lot_quality.act_lot_2_quality_meassure')
        all_child = self.with_context(active_test=False).search([('id', 'in', self.ids)])
        action["domain"] = [("lot_id", "in", all_child.ids)]
        return action

