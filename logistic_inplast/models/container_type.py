from odoo import _, api, fields, models

class ContainerType(models.Model):
    _name = "container.type"
    _description = "Container type"

    name = fields.Char("Name", related='container_type_id.name')
    container_type_id = fields.Many2one('container.type', string='Type')
    type = fields.Selection(
        [
            ("truck", "Truck"),
            ("container", "Container"),
            ("plane", "Plane"),
        ],
        string="Type",
        required=True,
    )
    description = fields.Html('Description')
