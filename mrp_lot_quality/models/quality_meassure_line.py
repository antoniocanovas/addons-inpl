# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class QualityMeassureLine(models.Model):
    _name = "quality.meassure.line"
    _description = "Quality results"

    lot_id = fields.Many2one('stock.lot', string="Lot")
    figure = fields.Integer("Figure")
    external_plate = fields.Float("External plate")
    internal_without_screw = fields.Float("Internal without screw")
    total_internal = fields.Float("Internal")
    total_height = fields.Float("total_height")
