from odoo import _, api, fields, models

class ContainerType(models.Model):
    _name = "container.type"
    _description = "Container type"

    name = fields.Many2one("container.type", string="Name")
    sequence = fields.Integer('Sequence')
    partner_id = fields.Many2one('res.partner', string="Partner")