from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    container_id = fields.Many2one("container.type", related="sale_id.container_id")

    pnt_truck_license_plate = fields.Char(string="Truck License Plate")
    pnt_trailer_license_plate = fields.Char(string="Trailer License Plate")
    pnt_container_number = fields.Char(string="Container Number")
    pnt_security_seal = fields.Char(string="Security Seal")
