from odoo import _, api, fields, models

class ContainerTypeLine(models.Model):
    _name = "container.type.line"
    _description = "Container type line"

    name = fields.Many2one("container.type", string="Name")
    sequence = fields.Integer('Sequence')
    partner_id = fields.Many2one('res.partner', string="Partner")
    container_type_id = fields.Many2one('container.type', string="Container")