
from odoo import api, fields, models, _



class FrontdesckVisitor(models.Model):
    _inherit = "frontdesk.visitor"

    security_level = fields.Selection([('visitor','Visitor'),('external','External')], string= 'Security level')

