
from odoo import api, fields, models, _



class FrontdesckVisitor(models.Model):
    _inherit = "frontdesk.visitor"

    security_level = fields.Selection([('fabric','Fabric'),('office','Office')], string= 'Security level')
